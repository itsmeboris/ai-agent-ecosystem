# Cursor Custom Commands

This directory contains custom slash commands for Cursor IDE to enhance your development workflow with AI assistance.

## Available Commands

### `/code-review`
Performs comprehensive code review focusing on security, performance, and code quality.

**Usage:**
```
/code-review @src/api/users.ts
```

### `/add-tests`
Generates comprehensive unit tests with proper coverage for selected code.

**Usage:**
```
/add-tests @src/utils/validation.ts
```

### `/security-audit`
Conducts security analysis based on OWASP Top 10 vulnerabilities.

**Usage:**
```
/security-audit @src/api/
```

### `/optimize-performance`
Identifies and resolves performance bottlenecks in code.

**Usage:**
```
/optimize-performance @src/api/orders.ts
```

### `/generate-api-docs`
Creates OpenAPI/Swagger documentation for API endpoints.

**Usage:**
```
/generate-api-docs @src/api/
```

## Installation

These commands are automatically installed to `~/.cursor/commands/` when you run:

```bash
# Using bash script
./install-agents.sh

# Or using Python script
python3 install-agents.py
```

## Manual Installation

To install manually:

```bash
# Create commands directory if it doesn't exist
mkdir -p ~/.cursor/commands

# Copy all command files
cp commands/*.md ~/.cursor/commands/
```

## Usage in Cursor

1. Open Cursor IDE
2. Open the AI chat (Cmd/Ctrl + L)
3. Type `/` to see available commands
4. Select a command from the dropdown
5. The command prompt will be inserted
6. Add context with @ symbols (e.g., `@filename.ts`)
7. Press Enter to execute

## Customization

You can customize these commands by:

1. Editing the `.md` files in this directory
2. Running the install script again to update `~/.cursor/commands/`
3. Or directly editing the files in `~/.cursor/commands/`

## Creating New Commands

To create a new command:

1. Create a new `.md` file in this directory (e.g., `my-command.md`)
2. Follow the structure of existing commands:
   - Clear role definition
   - Specific requirements
   - Expected output format
3. Run the install script to deploy
4. The command will be available as `/my-command` in Cursor

## Best Practices

- **Be Specific**: Include clear objectives and requirements
- **Provide Context**: Use @ symbols to reference files and folders
- **Set Boundaries**: Define constraints and scope
- **Show Examples**: Include expected output formats
- **Iterate**: Refine commands based on results

## More Information

For comprehensive guides on Cursor + Claude integration:

- **Quick Start**: `CURSOR_QUICKSTART_TEMPLATES.md`
- **Full Guide**: `CURSOR_ENHANCEMENT_GUIDE.md`
- **Advanced Techniques**: `CLAUDE_PROMPT_OPTIMIZATION.md`
- **Navigation**: `CURSOR_CLAUDE_INTEGRATION_INDEX.md`

