# AWS CLI Auto-Completion

AWS CLI auto-completion provides tab-completion for commands, subcommands, options, and parameter values in your terminal.

## Enabling Auto-Completion

### Bash (Linux/macOS)
```bash
# For AWS CLI v2 - add to ~/.bashrc or ~/.bash_profile
complete -C '/usr/local/bin/aws_completer' aws

# Or via the AWS CLI (v2)
aws --completer >> ~/.bashrc
source ~/.bashrc
```

### Zsh (macOS default)
```bash
# For AWS CLI v2 - add to ~/.zshrc
echo "autoload bashcompinit && bashcompinit" >> ~/.zshrc
echo "complete -C '/usr/local/bin/aws_completer' aws" >> ~/.zshrc
source ~/.zshrc
```

### Fish Shell
```fish
# For fish shell
echo "complete --command aws --no-files --arguments '(aws_completer (commandline -cp))'" >> ~/.config/fish/config.fish
```

## How It Works

```bash
# Type partial command and press Tab
aws s3 <Tab>            # Shows: ls mb presign rb rm sync website
aws ec2 describe-<Tab>  # Shows: describe-account-attributes describe-addresses describe-availability-zones...
aws s3api put-bucket-<Tab>  # Shows: put-bucket-acl put-bucket-analytics-configuration put-bucket-policy...
```

## Verification

```bash
# Test if auto-completion is working
aws <Tab><Tab>  # Should list all AWS CLI commands

# Check completer location
which aws_completer
# Output: /usr/local/bin/aws_completer
```

## Advanced Usage

### Custom Completion for Scripts
```bash
# Create a custom completer for your scripts
#!/bin/bash
_my_aws_script() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $(compgen -W "deploy list status rollback" -- $cur) )
    fi
}
complete -F _my_aws_script my-aws-script
```

### AWS CLI v2 Auto-Prompt (Alternative)
```bash
# AWS CLI v2 has a built-in auto-prompt feature
export AWS_CLI_AUTO_PROMPT=on

# Now you get interactive prompts without needing shell completion
aws s3 ls
# ? >  (interactive TUI)
```

## Troubleshooting

```bash
# If completion isn't working:
# 1. Verify AWS CLI v2 installation
aws --version

# 2. Check completer exists
ls -la /usr/local/bin/aws_completer

# 3. Ensure shell config is sourced
grep "aws_completer" ~/.bashrc ~/.zshrc 2>/dev/null

# 4. Test directly
/usr/local/bin/aws_completer "aws s3"
```

## Exam Tips

- ✅ **AWS CLI v2** includes the completer; v1 requires separate installation
- ✅ Completions work for **commands, subcommands, options, and S3 paths**
- ✅ **Bash/Zsh** require `complete -C` command in shell config
- ✅ **Auto-prompt** (`AWS_CLI_AUTO_PROMPT=on`) is an alternative to shell completion in v2
- ✅ Completions **do NOT work for resource names** (bucket names, instance IDs)
- ✅ S3 paths **do work** with completion (`aws s3 ls s3://<Tab>`)

## Q&A

**Q1: How do you enable AWS CLI auto-completion in bash?**
A: Add `complete -C '/usr/local/bin/aws_completer' aws` to `~/.bashrc`.

**Q2: What is the difference between auto-completion and auto-prompt in AWS CLI v2?**
A: Auto-completion uses shell tab-completion; auto-prompt provides interactive TUI prompts when `AWS_CLI_AUTO_PROMPT=on`.

**Q3: Does auto-completion work for S3 bucket paths?**
A: Yes, S3 paths like `s3://bucket-name/` support tab-completion.

**Q4: What command verifies the AWS completer is installed?**
A: `which aws_completer`

**Q5: Does auto-completion work for resource ARNs or instance IDs?**
A: No, only commands, subcommands, options, and S3 paths.

**Q6: How do you enable auto-completion in Zsh on macOS?**
A: Add `autoload bashcompinit && bashcompinit` and `complete -C '/usr/local/bin/aws_completer' aws` to `~/.zshrc`.

**Q7: What environment variable enables AWS CLI v2 auto-prompt?**
A: `export AWS_CLI_AUTO_PROMPT=on`