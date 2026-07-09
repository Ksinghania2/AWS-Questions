# AWS CLI Auto-Prompt (v2 Feature)

AWS CLI v2 introduced an interactive auto-prompt mode that provides a guided, menu-driven experience for building AWS CLI commands.

## What is Auto-Prompt?

Auto-prompt is an interactive TUI (Terminal User Interface) that guides you through command construction with:
- Dropdown menus for commands and options
- Auto-completion for required parameters
- Interactive selection for enum values
- Help text inline

## Enabling Auto-Prompt

### Method 1: Environment Variable
```bash
# Enable for current session
export AWS_CLI_AUTO_PROMPT=on

# Run a command interactively
aws s3 ls
# ? >  (Interactive TUI opens)
```

### Method 2: Per-Command
```bash
# Enable for a single command
aws --cli-auto-prompt s3 ls
```

### Method 3: Config File
```bash
# Add to ~/.aws/config
[default]
cli_auto_prompt = on

# For specific profile
[profile dev]
cli_auto_prompt = on
```

### Method 4: Shell Config (Permanent)
```bash
# Add to ~/.bashrc or ~/.zshrc
export AWS_CLI_AUTO_PROMPT=on
```

## Interactive Features

```bash
# Enable auto-prompt
export AWS_CLI_AUTO_PROMPT=on

# Now type: aws ec2 describe-instances
# You'll see:
# ? region:  us-east-1 (interactive)
# ? instance-ids:  (optional, press Enter to skip)
# ? output:  json (select from dropdown)
```

## Auto-Prompt Modes

### on (Partial)
```bash
# Only prompts when command is incomplete
aws s3 ls s3://my-bucket  # Works normally
aws s3                    # Opens auto-prompt
```

### on-partial (Default-like)
```bash
# Only prompts for missing required parameters
aws ec2 describe-instances --instance-ids  # Prompts for instance-ids
```

### on (Full)
```bash
# Always opens interactive prompt
export AWS_CLI_AUTO_PROMPT=on-partial
```

## Navigation Keys

| Key | Action |
|-----|--------|
| `Tab` / `Down Arrow` | Next option |
| `Up Arrow` | Previous option |
| `Enter` | Select/Confirm |
| `Space` | Toggle selection (multi-select) |
| `Ctrl+C` | Cancel |
| `?` | Help for current option |

## Examples

### Creating an S3 Bucket
```bash
export AWS_CLI_AUTO_PROMPT=on

# Type: aws s3api create-bucket
# Interactive prompts:
# ? bucket:  my-interactive-bucket
# ? create-bucket-configuration LocationConstraint:  (select from regions)
# ? output:  json
```

### Launching an EC2 Instance
```bash
export AWS_CLI_AUTO_PROMPT=on

# Type: aws ec2 run-instances
# Interactive prompts guide through:
# 1. Image ID (AMI)
# 2. Instance type
# 3. Key pair
# 4. Security groups
# 5. Subnet
```

## Disabling Auto-Prompt

```bash
# Temporarily disable for a command
AWS_CLI_AUTO_PROMPT=off aws s3 ls

# Remove from environment
unset AWS_CLI_AUTO_PROMPT
```

## Scripting vs Interactive

```bash
# Auto-prompt does NOT work in scripts
# BAD: This will hang in a script
aws s3api create-bucket  # Prompts interactively

# GOOD: Use full command for scripts
aws s3api create-bucket --bucket my-bucket --region us-east-1

# GOOD: Disable auto-prompt in scripts
AWS_CLI_AUTO_PROMPT=off aws s3api create-bucket --bucket my-bucket
```

## Exam Tips

- ✅ **AWS CLI v2 only** - Not available in v1
- ✅ **Environment variable**: `AWS_CLI_AUTO_PROMPT=on`
- ✅ **Config file**: `cli_auto_prompt = on` in `~/.aws/config`
- ✅ **Per-command**: `aws --cli-auto-prompt` flag
- ✅ **Does NOT work in scripts** - designed for interactive use only
- ✅ **Partial mode** (`on-partial`) only prompts for missing required parameters
- ✅ **Helpful for learning** new AWS CLI commands

## Q&A

**Q1: What is the difference between auto-completion and auto-prompt?**
A: Auto-completion uses shell tab-completion; auto-prompt provides interactive TUI menus with dropdown selection.

**Q2: How do you enable auto-prompt permanently?**
A: Add `export AWS_CLI_AUTO_PROMPT=on` to `~/.bashrc` or `~/.zshrc`, or set `cli_auto_prompt = on` in `~/.aws/config`.

**Q3: Can auto-prompt be used in shell scripts?**
A: No, auto-prompt is interactive and will hang in scripts. Use `AWS_CLI_AUTO_PROMPT=off` in scripts.

**Q4: What AWS CLI version supports auto-prompt?**
A: AWS CLI v2 only.

**Q5: What is the difference between `on` and `on-partial` modes?**
A: `on` always prompts; `on-partial` only prompts when required parameters are missing.

**Q6: How do you disable auto-prompt for a single command?**
A: Use `AWS_CLI_AUTO_PROMPT=off aws s3 ls`.

**Q7: What are the navigation keys in auto-prompt?**
A: Tab/arrows for navigation, Enter to confirm, Space for multi-select, Ctrl+C to cancel.