#!/bin/bash
# AI Agent Ecosystem Installer - Shell Script Version
#
# Shell script to copy agents and required documentation files from the repository 
# to .cursor/rules directory. Dynamically discovers available agents and categories.
#
# Required Documentation Files:
# - AGENT_HIERARCHY.md (agent coordination hierarchy)
# - WORKSPACE_PROTOCOLS.md (workspace management standards)
# - TEAM_COLLABORATION_CULTURE.md (communication guidelines)
# - AGENT_DIRECTORY.md (agent list and collaboration patterns)
# - agent-coordination-guide.md (coordination methodologies)
#
# Usage:
#   ./install-agents.sh <target_directory> [options]
#   ./install-agents.sh ~/.cursor/rules
#   ./install-agents.sh ~/.cursor/rules --category coordination core-technical
#   ./install-agents.sh ~/.cursor/rules --agents strategic-task-planner ai-ml-specialist

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_DIR="$SCRIPT_DIR/agents"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

usage() {
    echo "🎯 AI Agent Ecosystem Installer"
    echo ""
    echo "Usage: $0 <target_directory> [options]"
    echo ""
    echo "Arguments:"
    echo "  target_directory      Path to your .cursor/rules directory"
    echo ""
    echo "Options:"
    echo "  --all                Install all available agents"
    echo "  --category CAT...    Install agents from specific categories"
    echo "  --agents AGENT...    Install specific agents by name"
    echo "  --list-categories    List all available categories"
    echo "  --list-agents        List all available agents"
    echo "  --list-by-category   List agents organized by category"
    echo "  --dry-run           Show what would be copied without copying"
    echo "  --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 ~/.cursor/rules --all"
    echo "  $0 ~/.cursor/rules --category coordination core-technical"
    echo "  $0 ~/.cursor/rules --agents strategic-task-planner ai-ml-specialist"
    echo "  $0 --list-categories"
    echo ""
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_prerequisites() {
    # Check if agents directory exists
    if [[ ! -d "$AGENTS_DIR" ]]; then
        log_error "Agents directory not found at $AGENTS_DIR"
        log_error "Make sure you're running this script from the AI Agent Ecosystem repository root"
        exit 1
    fi

    log_info "Found agents directory at $AGENTS_DIR"
}

discover_categories() {
    # Return list of available categories
    local categories=()
    if [[ -d "$AGENTS_DIR" ]]; then
        for category_dir in "$AGENTS_DIR"/*/; do
            if [[ -d "$category_dir" ]]; then
                local category_name=$(basename "$category_dir")
                categories+=("$category_name")
            fi
        done
    fi
    printf '%s\n' "${categories[@]}"
}

discover_agents_in_category() {
    local category="$1"
    local category_dir="$AGENTS_DIR/$category"
    local agents=()

    if [[ -d "$category_dir" ]]; then
        for agent_file in "$category_dir"/*.mdc; do
            if [[ -f "$agent_file" ]]; then
                local agent_name=$(basename "$agent_file" .mdc)
                agents+=("$agent_name")
            fi
        done
    fi
    printf '%s\n' "${agents[@]}"
}

find_agent_category() {
    local agent_name="$1"
    local categories
    mapfile -t categories < <(discover_categories)

    for category in "${categories[@]}"; do
        local agents
        mapfile -t agents < <(discover_agents_in_category "$category")
        for agent in "${agents[@]}"; do
            if [[ "$agent" == "$agent_name" ]]; then
                echo "$category"
                return 0
            fi
        done
    done
    return 1
}

get_category_description() {
    local category="$1"
    local readme_file="$AGENTS_DIR/$category/README.md"

    if [[ -f "$readme_file" ]]; then
        # Read first non-empty, non-header line as description
        while IFS= read -r line; do
            line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            if [[ -n "$line" && ! "$line" =~ ^# ]]; then
                echo "$line"
                return 0
            fi
        done < "$readme_file"
    fi

    # Fallback to formatted category name
    echo "$category" | sed 's/-/ /g' | sed 's/\b\w/\U&/g'
}

validate_target_directory() {
    local target_dir="$1"

    # Expand tilde and resolve path
    target_dir="${target_dir/#\~/$HOME}"
    target_dir="$(realpath -m "$target_dir")"

    # Create directory if it doesn't exist
    if [[ ! -d "$target_dir" ]]; then
        log_info "Creating target directory: $target_dir"
        mkdir -p "$target_dir" || {
            log_error "Failed to create target directory: $target_dir"
            exit 1
        }
    fi

    # Check if directory is writable
    if [[ ! -w "$target_dir" ]]; then
        log_error "Target directory is not writable: $target_dir"
        exit 1
    fi

    echo "$target_dir"
}

copy_agent() {
    local agent_name="$1"
    local source_category="$2"
    local target_dir="$3"
    local category_dir="$AGENTS_DIR/$source_category"
    local source_file="$category_dir/$agent_name.mdc"
    local target_file="$target_dir/$agent_name.mdc"

    if [[ ! -f "$source_file" ]]; then
        log_warning "Agent $agent_name not found in $source_category"
        return 1
    fi

    if cp "$source_file" "$target_file"; then
        log_success "Copied $agent_name.mdc"
        return 0
    else
        log_error "Failed to copy $agent_name.mdc"
        return 1
    fi
}

copy_documentation_files() {
    local target_dir="$1"
    local docs_copied=0
    local total_docs=5
    
    # Define required documentation files
    declare -A doc_files=(
        ["AGENT_HIERARCHY.md"]="$AGENTS_DIR/coordination/AGENT_HIERARCHY.md"
        ["WORKSPACE_PROTOCOLS.md"]="$AGENTS_DIR/coordination/WORKSPACE_PROTOCOLS.md"
        ["TEAM_COLLABORATION_CULTURE.md"]="$AGENTS_DIR/coordination/TEAM_COLLABORATION_CULTURE.md"
        ["AGENT_DIRECTORY.md"]="$AGENTS_DIR/coordination/AGENT_DIRECTORY.md"
        ["agent-coordination-guide.md"]="$SCRIPT_DIR/docs/agent-coordination-guide.md"
    )
    
    for filename in "${!doc_files[@]}"; do
        local source_file="${doc_files[$filename]}"
        local target_file="$target_dir/$filename"
        
        if [[ ! -f "$source_file" ]]; then
            log_warning "$filename not found at $source_file"
            continue
        fi
        
        if cp "$source_file" "$target_file"; then
            log_success "Copied $filename"
            ((docs_copied++))
        else
            log_error "Failed to copy $filename"
        fi
    done
    
    echo "$docs_copied"
}

install_agents() {
    local target_dir="$1"
    local mode="$2"
    shift 2
    local items=("$@")
    local total_copied=0
    local total_agents=0
    local hierarchy_copied=false

    # Always copy required documentation files first
    log_info "Copying required documentation files..."
    local docs_copied
    docs_copied=$(copy_documentation_files "$target_dir")
    local hierarchy_copied=false
    if [[ -f "$target_dir/AGENT_HIERARCHY.md" ]]; then
        hierarchy_copied=true
    fi

    case "$mode" in
        "all")
            log_info "Installing all available agents..."
            local categories
            mapfile -t categories < <(discover_categories)

            for category in "${categories[@]}"; do
                local agents
                mapfile -t agents < <(discover_agents_in_category "$category")

                if [[ ${#agents[@]} -gt 0 ]]; then
                    echo ""
                    log_info "Installing $category agents:"

                    for agent in "${agents[@]}"; do
                        if copy_agent "$agent" "$category" "$target_dir"; then
                            ((total_copied++))
                        fi
                        ((total_agents++))
                    done
                fi
            done
            ;;

        "categories")
            log_info "Installing selected categories: ${items[*]}"

            for category in "${items[@]}"; do
                local agents
                mapfile -t agents < <(discover_agents_in_category "$category")

                if [[ ${#agents[@]} -eq 0 ]]; then
                    log_warning "No agents found in category: $category"
                    continue
                fi

                echo ""
                log_info "Installing $category agents:"

                for agent in "${agents[@]}"; do
                    if copy_agent "$agent" "$category" "$target_dir"; then
                        ((total_copied++))
                    fi
                    ((total_agents++))
                done
            done
            ;;

        "agents")
            log_info "Installing specific agents: ${items[*]}"

            for agent_name in "${items[@]}"; do
                local category
                if category=$(find_agent_category "$agent_name"); then
                    if copy_agent "$agent_name" "$category" "$target_dir"; then
                        ((total_copied++))
                    fi
                else
                    log_warning "Agent $agent_name not found in any category"
                fi
                ((total_agents++))
            done
            ;;
    esac

    # Summary
    echo ""
    echo "🎯 Installation Summary:"
    echo "   ✅ Successfully copied: $total_copied agents"
    echo "   ✅ Documentation files: $docs_copied/5 copied successfully"
    if [[ $total_agents -gt $total_copied ]]; then
        echo "   ⚠️  Failed or skipped: $((total_agents - total_copied)) agents"
    fi
    echo "   📁 Target directory: $target_dir"
    echo ""

    if [[ $total_copied -gt 0 ]]; then
        log_success "Installation complete!"
        echo "🚀 Ready to use! Restart your IDE to load the new agents."
        echo "   Test with: @strategic-task-planner: Hello"
        if [[ "$hierarchy_copied" == true ]]; then
            echo "   📋 Agent coordination enabled with full documentation support"
            echo "   📖 Coordination guide: See agent-coordination-guide.md"
        fi
    else
        log_warning "No agents were installed."
    fi
}

list_categories() {
    echo "📋 Available Agent Categories:"
    echo ""

    local categories
    mapfile -t categories < <(discover_categories | sort)

    if [[ ${#categories[@]} -eq 0 ]]; then
        log_error "No agent categories found"
        return 1
    fi

    for category in "${categories[@]}"; do
        local agents
        mapfile -t agents < <(discover_agents_in_category "$category")
        local agent_count=${#agents[@]}
        local description
        description=$(get_category_description "$category")

        echo -e "${CYAN}📂 $category${NC} ($agent_count agents)"
        echo "   $description"

        if [[ $agent_count -gt 0 ]]; then
            for agent in "${agents[@]}"; do
                echo "   • $agent"
            done
        fi
        echo ""
    done
}

list_agents() {
    echo "🤖 All Available Agents:"
    echo ""

    local all_agents=()
    local agent_locations=()
    local categories
    mapfile -t categories < <(discover_categories)

    for category in "${categories[@]}"; do
        local agents
        mapfile -t agents < <(discover_agents_in_category "$category")
        for agent in "${agents[@]}"; do
            all_agents+=("$agent")
            agent_locations+=("$category")
        done
    done

    if [[ ${#all_agents[@]} -eq 0 ]]; then
        log_error "No agents found"
        return 1
    fi

    # Sort agents with their locations
    local sorted_indices
    mapfile -t sorted_indices < <(printf '%s\n' "${!all_agents[@]}" | sort -k1,1 -t$'\t' --key=<(printf '%s\n' "${all_agents[@]}" | nl -nln | sort -k2))

    echo "Total: ${#all_agents[@]} agents"
    echo ""

    local i=1
    for agent in $(printf '%s\n' "${all_agents[@]}" | sort); do
        local category
        category=$(find_agent_category "$agent")
        printf "%2d. %-35s (from %s)\n" "$i" "$agent" "$category"
        ((i++))
    done
}

list_by_category() {
    echo "🤖 Available Agents by Category:"
    echo ""

    local categories
    mapfile -t categories < <(discover_categories | sort)

    if [[ ${#categories[@]} -eq 0 ]]; then
        log_error "No agent categories found"
        return 1
    fi

    for category in "${categories[@]}"; do
        local agents
        mapfile -t agents < <(discover_agents_in_category "$category" | sort)

        if [[ ${#agents[@]} -gt 0 ]]; then
            echo -e "${CYAN}📂 $category:${NC}"
            for agent in "${agents[@]}"; do
                echo "   • $agent"
            done
            echo ""
        fi
    done
}

main() {
    # Parse arguments
    local target_dir=""
    local mode=""
    local items=()
    local dry_run=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                usage
                exit 0
                ;;
            --all)
                mode="all"
                shift
                ;;
            --category|--categories)
                mode="categories"
                shift
                while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                    items+=("$1")
                    shift
                done
                ;;
            --agents|--agent)
                mode="agents"
                shift
                while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                    items+=("$1")
                    shift
                done
                ;;
            --list-categories)
                check_prerequisites
                list_categories
                exit 0
                ;;
            --list-agents)
                check_prerequisites
                list_agents
                exit 0
                ;;
            --list-by-category)
                check_prerequisites
                list_by_category
                exit 0
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            -*)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
            *)
                if [[ -z "$target_dir" ]]; then
                    target_dir="$1"
                else
                    log_error "Multiple target directories specified"
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Validate arguments
    if [[ -z "$target_dir" ]]; then
        log_error "Target directory is required"
        usage
        exit 1
    fi

    if [[ -z "$mode" ]]; then
        log_error "Must specify --all, --category, or --agents"
        usage
        exit 1
    fi

    if [[ "$mode" == "categories" && ${#items[@]} -eq 0 ]]; then
        log_error "Must specify at least one category with --category"
        exit 1
    fi

    if [[ "$mode" == "agents" && ${#items[@]} -eq 0 ]]; then
        log_error "Must specify at least one agent with --agents"
        exit 1
    fi

    echo "🎯 AI Agent Ecosystem Installer"
    echo ""

    # Validate prerequisites
    check_prerequisites

    # Validate categories if specified
    if [[ "$mode" == "categories" ]]; then
        local available_categories
        mapfile -t available_categories < <(discover_categories)
        for category in "${items[@]}"; do
            if [[ ! " ${available_categories[*]} " =~ " $category " ]]; then
                log_error "Category '$category' not found"
                echo "Available categories:"
                for cat in "${available_categories[@]}"; do
                    echo "  • $cat"
                done
                exit 1
            fi
        done
    fi

    # Validate and prepare target directory
    target_dir=$(validate_target_directory "$target_dir")
    log_success "Target directory ready: $target_dir"
    echo ""

    if [[ "$dry_run" == true ]]; then
        echo "🔍 DRY RUN MODE - No files will be copied"
        echo ""
    fi

    # Install agents
    if [[ "$dry_run" == false ]]; then
        install_agents "$target_dir" "$mode" "${items[@]}"
    else
        echo "📋 Would install agents based on your selection:"
        case "$mode" in
            "all")
                echo "  • All available agents"
                ;;
            "categories")
                echo "  • Categories: ${items[*]}"
                ;;
            "agents")
                echo "  • Specific agents:"
                for agent in "${items[@]}"; do
                    local category
                    if category=$(find_agent_category "$agent"); then
                        echo "    - $agent (from $category)"
                    else
                        echo "    - $agent (NOT FOUND)"
                    fi
                done
                ;;
        esac
    fi
}

# Run main function
main "$@"