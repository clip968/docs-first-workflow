# Workflow Implementation

Use this file as the remote bootstrap instruction for installing docs-first
workflow in an existing repository. The target repository does not need to copy
this file locally; an agent can read the GitHub URL directly.

Agent instruction:

1. Read this file first.
2. Run the installer in dry-run mode.
3. Show the user the install summary, changed/created files, and resulting tree.
4. Ask: "Install this workflow now?"
5. Run the installer again with `--apply` only after the user explicitly agrees.

The installer auto-detects project name, language, source directory, test
directory, and test command from repository files. Users do not need to fill in
YAML for standard repositories.

Optional overrides:

```yaml
# project_name: "{{PROJECT_NAME}}"
# language: "{{LANGUAGE}}"
# source_dir: "{{SOURCE_DIR}}"
# test_dir: "{{TEST_DIR}}"
# test_command: "{{TEST_COMMAND}}"
install_mode: dry-run-first
```

Dry-run command:

```bash
python /path/to/docs-first-workflow/scripts/install_into_repo.py \
  --target . \
  --template-root /path/to/docs-first-workflow \
  --bootstrap-url https://github.com/clip968/docs-first-workflow/blob/main/workflow-implementation.md
```

Apply command after explicit approval:

```bash
python /path/to/docs-first-workflow/scripts/install_into_repo.py \
  --target . \
  --template-root /path/to/docs-first-workflow \
  --bootstrap-url https://github.com/clip968/docs-first-workflow/blob/main/workflow-implementation.md \
  --apply
```
