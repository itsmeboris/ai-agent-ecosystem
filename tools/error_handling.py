#!/usr/bin/env python3
"""
Error Handling Utilities for AI Agent Ecosystem
Provides reusable error handling patterns for all agents
"""

import time
import json
import os
import functools
import traceback
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Tuple, Dict, Any, Optional
from enum import Enum


class ErrorType(Enum):
    """Error classification types"""
    RECOVERABLE = "recoverable"
    ESCALATION = "escalation"
    CRITICAL = "critical"


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AgentError(Exception):
    """Base exception for agent errors"""
    def __init__(self, message: str, error_type: ErrorType, severity: ErrorSeverity,
                 context: Optional[Dict] = None):
        super().__init__(message)
        self.error_type = error_type
        self.severity = severity
        self.context = context or {}
        self.timestamp = datetime.now().isoformat()


class RecoverableError(AgentError):
    """Error that can be automatically recovered"""
    def __init__(self, message: str, severity: ErrorSeverity = ErrorSeverity.LOW,
                 context: Optional[Dict] = None):
        super().__init__(message, ErrorType.RECOVERABLE, severity, context)


class EscalationError(AgentError):
    """Error requiring coordination or specialist input"""
    def __init__(self, message: str, severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                 context: Optional[Dict] = None):
        super().__init__(message, ErrorType.ESCALATION, severity, context)


class CriticalError(AgentError):
    """Error requiring user intervention"""
    def __init__(self, message: str, severity: ErrorSeverity = ErrorSeverity.CRITICAL,
                 context: Optional[Dict] = None):
        super().__init__(message, ErrorType.CRITICAL, severity, context)


def retry_with_backoff(max_attempts: int = 3, base_delay: float = 1.0,
                       backoff_factor: int = 2, exceptions: Tuple = (Exception,)):
    """
    Decorator for retrying operations with exponential backoff

    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay (default: 2 for exponential)
        exceptions: Tuple of exceptions to catch and retry

    Example:
        @retry_with_backoff(max_attempts=3, base_delay=1)
        def fetch_api_data():
            return api.get('/data')
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)

                    # Log successful recovery if not first attempt
                    if attempt > 1:
                        _log_recovery(
                            operation=func.__name__,
                            attempt=attempt,
                            status="recovered"
                        )

                    return result

                except exceptions as e:
                    last_exception = e

                    if attempt == max_attempts:
                        # Log failure after all retries
                        _log_recovery(
                            operation=func.__name__,
                            attempt=attempt,
                            status="failed",
                            error=str(e)
                        )
                        raise RecoverableError(
                            f"Failed after {max_attempts} attempts: {str(e)}",
                            context={
                                'function': func.__name__,
                                'attempts': max_attempts,
                                'error': str(e)
                            }
                        ) from e

                    # Calculate delay with exponential backoff
                    delay = base_delay * (backoff_factor ** (attempt - 1))

                    # Log retry attempt
                    _log_recovery(
                        operation=func.__name__,
                        attempt=attempt,
                        status="retrying",
                        delay=delay,
                        error=str(e)
                    )

                    time.sleep(delay)

            # Should never reach here, but just in case
            raise last_exception

        return wrapper
    return decorator


def try_alternatives(*approaches: Tuple[str, Callable]) -> Tuple[str, Any]:
    """
    Try multiple approaches in order until one succeeds

    Args:
        approaches: Variable number of (name, function) tuples

    Returns:
        (approach_name, result) tuple

    Raises:
        RecoverableError if all approaches fail

    Example:
        name, data = try_alternatives(
            ("API", lambda: fetch_from_api()),
            ("Cache", lambda: fetch_from_cache()),
            ("Database", lambda: fetch_from_db())
        )
    """
    errors = []

    for name, approach_func in approaches:
        try:
            result = approach_func()

            # Log successful alternative
            _log_alternative(
                approach=name,
                attempted_count=len(errors) + 1,
                total_approaches=len(approaches),
                status="success"
            )

            return (name, result)

        except Exception as e:
            errors.append({
                'approach': name,
                'error': str(e),
                'traceback': traceback.format_exc()
            })

            # Log failed attempt
            _log_alternative(
                approach=name,
                attempted_count=len(errors),
                total_approaches=len(approaches),
                status="failed",
                error=str(e)
            )

    # All approaches failed
    raise RecoverableError(
        f"All {len(approaches)} approaches failed",
        context={'errors': errors}
    )


def with_graceful_degradation(critical_operations: List[str]):
    """
    Decorator for operations with graceful degradation

    Args:
        critical_operations: List of operation names that are critical (must succeed)

    Example:
        @with_graceful_degradation(critical_operations=['get_user', 'get_email'])
        def get_user_profile(user_id):
            result = {}
            result['user'] = get_user(user_id)  # Critical
            result['email'] = get_email(user_id)  # Critical
            result['avatar'] = get_avatar(user_id)  # Optional
            return result
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            degraded_mode = False
            missing_features = []

            # Execute function with degradation tracking
            try:
                result = func(*args, **kwargs)

                # Add degradation metadata if result is a dict
                if isinstance(result, dict):
                    result['_degraded_mode'] = degraded_mode
                    result['_missing_features'] = missing_features

                return result

            except Exception as e:
                operation_name = getattr(e, '__operation__', 'unknown')

                if operation_name in critical_operations:
                    # Critical operation failed - cannot degrade
                    raise CriticalError(
                        f"Critical operation failed: {operation_name}",
                        context={
                            'operation': operation_name,
                            'error': str(e)
                        }
                    ) from e
                else:
                    # Optional operation failed - continue in degraded mode
                    degraded_mode = True
                    missing_features.append(operation_name)
                    _log_degradation(operation_name, str(e))

                    # Re-raise if not a dict result
                    raise

        return wrapper
    return decorator


class CheckpointManager:
    """Manage task checkpoints for recovery"""

    def __init__(self, task_id: str, checkpoint_dir: str = "workspaces/.checkpoints"):
        self.task_id = task_id
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_file = self.checkpoint_dir / f"{task_id}.json"

        # Ensure checkpoint directory exists
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(self, state: Dict[str, Any], description: str) -> None:
        """Save current state as checkpoint"""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'task_id': self.task_id,
            'description': description,
            'state': state
        }

        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)

        _log_checkpoint('saved', self.task_id, description)

    def restore_checkpoint(self) -> Optional[Dict[str, Any]]:
        """Restore from last checkpoint"""
        if not self.checkpoint_file.exists():
            return None

        with open(self.checkpoint_file, 'r') as f:
            checkpoint = json.load(f)

        _log_checkpoint('restored', self.task_id, checkpoint['description'])
        return checkpoint['state']

    def clear_checkpoint(self) -> None:
        """Clear checkpoint after successful completion"""
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()
        _log_checkpoint('cleared', self.task_id)

    def get_checkpoint_info(self) -> Optional[Dict[str, Any]]:
        """Get checkpoint metadata without restoring"""
        if not self.checkpoint_file.exists():
            return None

        with open(self.checkpoint_file, 'r') as f:
            checkpoint = json.load(f)

        return {
            'timestamp': checkpoint['timestamp'],
            'description': checkpoint['description'],
            'exists': True
        }


def with_checkpoint_recovery(task_id: str, checkpoint_interval: int = 100):
    """
    Decorator for functions that support checkpoint recovery

    Args:
        task_id: Unique identifier for this task
        checkpoint_interval: How often to save checkpoints (iterations)

    Example:
        @with_checkpoint_recovery(task_id='PROCESS-001', checkpoint_interval=100)
        def process_items(items):
            for i, item in enumerate(items):
                process_item(item)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            checkpoint_mgr = CheckpointManager(task_id)

            # Try to restore from checkpoint
            state = checkpoint_mgr.restore_checkpoint()
            if state:
                print(f"Resuming from checkpoint: {state}")
                kwargs['_checkpoint_state'] = state

            try:
                result = func(*args, **kwargs)

                # Success - clear checkpoint
                checkpoint_mgr.clear_checkpoint()
                return result

            except Exception as e:
                # Save checkpoint before failing
                if '_checkpoint_state' in kwargs:
                    checkpoint_mgr.save_checkpoint(
                        state=kwargs['_checkpoint_state'],
                        description=f"Failed: {str(e)}"
                    )
                raise

        return wrapper
    return decorator


class ErrorReporter:
    """Generate structured error reports"""

    @staticmethod
    def generate_report(error: AgentError, agent_name: str, task_id: str,
                        attempted_fixes: Optional[List[str]] = None,
                        recommendations: Optional[List[Dict]] = None) -> str:
        """
        Generate formatted error report for SHARED_PROGRESS.md

        Args:
            error: The AgentError instance
            agent_name: Name of the agent reporting the error
            task_id: ID of the task that failed
            attempted_fixes: List of fix attempts made
            recommendations: List of recommendation dicts with keys:
                            'option', 'pros', 'cons', 'effort_hours'

        Returns:
            Formatted markdown error report
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        status_emoji = {
            ErrorType.RECOVERABLE: "🔄",
            ErrorType.ESCALATION: "⚠️",
            ErrorType.CRITICAL: "❌"
        }
        status_text = {
            ErrorType.RECOVERABLE: "In Progress (Recovered from error)",
            ErrorType.ESCALATION: "Blocked - Escalation Required",
            ErrorType.CRITICAL: "Failed - User Intervention Required"
        }

        report = f"""## {timestamp} - @{agent_name}: {task_id}

**Status**: {status_emoji[error.error_type]} {status_text[error.error_type]}

**{error.error_type.value.title()} Error**:
- **Error Type**: {error.error_type.value}
- **Severity**: {error.severity.value.upper()}
- **Issue**: {str(error)}

**Context**:
"""

        # Add context details
        for key, value in error.context.items():
            if isinstance(value, (list, dict)):
                report += f"- **{key}**: ```{json.dumps(value, indent=2)}```\n"
            else:
                report += f"- **{key}**: {value}\n"

        # Add attempted fixes
        if attempted_fixes:
            report += "\n**Attempted Fixes**:\n"
            for fix in attempted_fixes:
                report += f"- {fix}\n"

        # Add recommendations
        if recommendations:
            report += "\n**Recommendations**:\n\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"**Option {i}: {rec['option']}**\n"
                if 'pros' in rec:
                    report += "- Pros:\n"
                    for pro in rec['pros']:
                        report += f"  - {pro}\n"
                if 'cons' in rec:
                    report += "- Cons:\n"
                    for con in rec['cons']:
                        report += f"  - {con}\n"
                if 'effort_hours' in rec:
                    report += f"- Effort: {rec['effort_hours']} hours\n"
                report += "\n"

        report += f"\n**Timestamp**: {error.timestamp}\n"

        return report


# Internal logging functions

def _log_recovery(operation: str, attempt: int, status: str,
                  delay: Optional[float] = None, error: Optional[str] = None) -> None:
    """Log recovery attempts"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': 'recovery',
        'operation': operation,
        'attempt': attempt,
        'status': status
    }

    if delay:
        log_entry['retry_delay_seconds'] = delay
    if error:
        log_entry['error'] = error

    _write_log(log_entry)


def _log_alternative(approach: str, attempted_count: int, total_approaches: int,
                     status: str, error: Optional[str] = None) -> None:
    """Log alternative approach attempts"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': 'alternative_approach',
        'approach': approach,
        'attempted_count': attempted_count,
        'total_approaches': total_approaches,
        'status': status
    }

    if error:
        log_entry['error'] = error

    _write_log(log_entry)


def _log_degradation(feature: str, error: str, level: str = 'warning') -> None:
    """Log graceful degradation events"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': 'degradation',
        'feature': feature,
        'level': level,
        'error': error
    }

    _write_log(log_entry)


def _log_checkpoint(action: str, task_id: str, description: str = None) -> None:
    """Log checkpoint operations"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': 'checkpoint',
        'action': action,
        'task_id': task_id
    }

    if description:
        log_entry['description'] = description

    _write_log(log_entry)


def _write_log(log_entry: Dict) -> None:
    """Write log entry to error handling log file"""
    log_file = Path("workspaces/.logs/error_handling.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


# Example usage and tests

if __name__ == '__main__':
    print("Error Handling Utilities - Examples")
    print("=" * 60)

    # Example 1: Retry with backoff
    print("\n1. Retry with Backoff:")

    @retry_with_backoff(max_attempts=3, base_delay=0.1)
    def unstable_api_call():
        import random
        if random.random() < 0.7:  # 70% failure rate
            raise ConnectionError("API temporarily unavailable")
        return {"data": "success"}

    try:
        result = unstable_api_call()
        print(f"   Success: {result}")
    except RecoverableError as e:
        print(f"   Failed after retries: {e}")

    # Example 2: Try alternatives
    print("\n2. Try Alternatives:")

    def primary_source():
        raise Exception("Primary failed")

    def backup_source():
        return {"source": "backup", "data": [1, 2, 3]}

    try:
        source, data = try_alternatives(
            ("Primary API", primary_source),
            ("Backup Source", backup_source)
        )
        print(f"   Used {source}: {data}")
    except RecoverableError as e:
        print(f"   All sources failed: {e}")

    # Example 3: Checkpoint recovery
    print("\n3. Checkpoint Recovery:")

    checkpoint_mgr = CheckpointManager("EXAMPLE-001")

    # Save checkpoint
    checkpoint_mgr.save_checkpoint(
        state={'processed': 50, 'total': 100},
        description="Halfway through processing"
    )
    print("   Checkpoint saved")

    # Restore checkpoint
    state = checkpoint_mgr.restore_checkpoint()
    print(f"   Checkpoint restored: {state}")

    # Clear checkpoint
    checkpoint_mgr.clear_checkpoint()
    print("   Checkpoint cleared")

    # Example 4: Error reporting
    print("\n4. Error Reporting:")

    error = EscalationError(
        "Security vulnerability detected",
        severity=ErrorSeverity.HIGH,
        context={
            'vulnerability_type': 'SQL Injection',
            'location': 'user-service.js:45',
            'risk_level': 'high'
        }
    )

    report = ErrorReporter.generate_report(
        error=error,
        agent_name="backend-architect",
        task_id="AUTH-001",
        attempted_fixes=["Added input sanitization", "Implemented prepared statements"],
        recommendations=[
            {
                'option': 'Full security audit',
                'pros': ['Comprehensive', 'Catches all issues'],
                'cons': ['Time consuming'],
                'effort_hours': 8
            }
        ]
    )

    print(report)

    print("\n" + "=" * 60)
    print("Examples complete. Check workspaces/.logs/error_handling.log for logs")
