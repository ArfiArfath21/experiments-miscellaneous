# GitHub Actions Comprehensive Cheatsheet

## Core Concepts

### Workflow Basics
- **Workflow**: Automated process configurable to build, test, package, release, or deploy code
- **Event**: Specific activity that triggers a workflow (push, pull request, etc.)
- **Job**: Set of steps executed on the same runner
- **Step**: Individual task that can run commands or actions
- **Action**: Standalone command used as a step in a workflow
- **Runner**: Server that runs workflows (GitHub-hosted or self-hosted)

### File Structure
- Workflows defined in `.github/workflows` directory
- YAML files with `.yml` or `.yaml` extension
- Each workflow file defines a separate workflow

## Workflow File Syntax

### Basic Structure
```yaml
name: Workflow Name                       # Optional workflow name

on: [push, pull_request]                  # Events that trigger the workflow

jobs:
  job_id:                                 # Unique job identifier
    name: Job Name                        # Optional job name
    runs-on: ubuntu-latest                # Runner environment
    
    steps:
      - name: Step name                   # Optional step name
        uses: actions/checkout@v4         # Action to use
      
      - name: Another step
        run: echo "Hello, world!"         # Command to run
```

### Event Triggers

#### Basic Events
```yaml
on: push                    # Single event
on: [push, pull_request]    # Multiple events
```

#### Advanced Event Configuration
```yaml
on:
  push:
    branches: [main, 'releases/**']
    branches-ignore: ['dev-*']
    tags: ['v*']
    paths: ['**.js', '!docs/**']
    paths-ignore: ['docs/**', '**.md']
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]
```

#### Schedule Events
```yaml
on:
  schedule:
    - cron: '0 0 * * *'     # Daily at midnight (UTC)
    - cron: '0 */3 * * *'   # Every 3 hours
```

#### Manual Triggers
```yaml
on:
  workflow_dispatch:        # Manual trigger from GitHub UI
    inputs:
      logLevel:
        description: 'Log level'
        required: true
        default: 'warning'
        type: choice
        options:
          - info
          - warning
          - debug

  repository_dispatch:      # External trigger via REST API
    types: [deploy, sync]
```

#### Other Events
```yaml
on:
  issue_comment:
    types: [created, edited]
  release:
    types: [published, created, edited]
  status:  # GitHub status
  watch:
    types: [started]  # When someone stars the repo
```

### Job Definition

#### Basic Job
```yaml
jobs:
  build:
    name: Build and Test
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Run tests
        run: npm test
```

#### Job Dependencies
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./build.sh
        
  test:
    needs: build  # This job depends on 'build' job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./test.sh
      
  deploy:
    needs: [build, test]  # This job depends on multiple jobs
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
```

#### Matrix Strategy
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [14.x, 16.x, 18.x]
        include:
          - os: ubuntu-latest
            node-version: 20.x
            experimental: true
        exclude:
          - os: macos-latest
            node-version: 14.x
      fail-fast: false  # Continue running matrix jobs if one fails
      max-parallel: 3   # Limit parallel jobs
    
    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

#### Conditional Execution
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        if: success() && github.repository == 'owner/repo-name'
        run: ./deploy.sh
```

### Step Definitions

#### Using Actions
```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4
    with:
      ref: main
      fetch-depth: 0
      token: ${{ secrets.GITHUB_TOKEN }}

  - name: Install Node.js
    uses: actions/setup-node@v4
    with:
      node-version: 16
      cache: 'npm'
```

#### Running Commands
```yaml
steps:
  - name: Install dependencies
    run: npm ci
  
  - name: Multi-line command
    run: |
      echo "First line"
      echo "Second line"
      ./complex-script.sh
    
  - name: Set environment for command
    env:
      NODE_ENV: production
    run: npm run build
  
  - name: Command with working directory
    working-directory: ./app
    run: npm test
  
  - name: Command with shell
    shell: bash
    run: |
      echo $SHELL
      bash -c 'echo $BASH_VERSION'
```

#### Conditional Steps
```yaml
steps:
  - name: Run on main branch
    if: github.ref == 'refs/heads/main'
    run: echo "This runs only on main branch"
  
  - name: Run on PR
    if: github.event_name == 'pull_request'
    run: echo "This runs only on pull requests"
  
  - name: Run if previous step succeeded
    if: success()
    run: echo "Previous step succeeded"
  
  - name: Always run
    if: always()
    run: echo "This always runs"
  
  - name: Run on failure
    if: failure()
    run: echo "A previous step failed"
```

### Environment and Secrets

#### Setting Environment Variables
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    
    # Job-level env vars (available to all steps)
    env:
      NODE_ENV: production
      SERVER: production-server
    
    steps:
      # Step-level env vars (only for this step)
      - name: Build
        env:
          CUSTOM_VAR: custom_value
        run: echo $NODE_ENV $CUSTOM_VAR
      
      # Workflow-command to set env var for subsequent steps
      - name: Set env var for next steps
        run: echo "ACTION_STATE=yellow" >> $GITHUB_ENV
      
      - name: Use environment variable
        run: echo $ACTION_STATE
```

#### Using Secrets
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy with secret
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
        run: ./deploy.sh
      
      - name: AWS authentication
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
```

### Outputs and Job Results

#### Setting and Using Outputs
```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    outputs:
      output1: ${{ steps.step1.outputs.test }}
      output2: ${{ steps.step2.outputs.result }}
    
    steps:
      - id: step1
        run: echo "test=hello" >> $GITHUB_OUTPUT
      
      - id: step2
        run: echo "result=success" >> $GITHUB_OUTPUT
  
  job2:
    runs-on: ubuntu-latest
    needs: job1
    steps:
      - run: echo ${{ needs.job1.outputs.output1 }}
      - run: echo ${{ needs.job1.outputs.output2 }}
```

#### Saving and Using Artifacts
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build
        run: npm run build
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-files
          path: |
            dist
            !dist/**/*.map
          retention-days: 5
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-files
          path: dist
      
      - name: Deploy
        run: ./deploy.sh
```

## Advanced Features

### Service Containers
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
        env:
          DB_HOST: localhost
          DB_PORT: 5432
```

### Self-Hosted Runners
```yaml
jobs:
  build:
    runs-on: self-hosted  # Use default self-hosted runner
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: ./build.sh
  
  test:
    runs-on: [self-hosted, linux, x64, gpu]  # Use runner with specific labels
    steps:
      - uses: actions/checkout@v4
      - name: Test
        run: ./test.sh
```

### Permissions
```yaml
# Workflow-level permissions
permissions:
  actions: read
  contents: write
  issues: write
  pull-requests: read

jobs:
  job1:
    runs-on: ubuntu-latest
    # Job-level permissions (override workflow permissions)
    permissions:
      contents: read
      deployments: write
    steps:
      - uses: actions/checkout@v4
```

### Concurrency
```yaml
# Limit concurrent workflow runs for same branch/PR
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel in-progress runs

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
```

### Reusable Workflows
```yaml
# Workflow 1: Reusable workflow (caller)
name: Main CI
on: [push, pull_request]

jobs:
  call-reusable-workflow:
    uses: ./.github/workflows/reusable-workflow.yml
    with:
      config-path: .github/labeler.yml
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

```yaml
# Workflow 2: Called workflow (callee)
name: Reusable workflow
on:
  workflow_call:
    inputs:
      config-path:
        required: true
        type: string
    secrets:
      token:
        required: true

jobs:
  reusable_job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/labeler@v4
        with:
          repo-token: ${{ secrets.token }}
          configuration-path: ${{ inputs.config-path }}
```

### Workflow Commands
```yaml
jobs:
  debug:
    runs-on: ubuntu-latest
    steps:
      # Set output for a step
      - name: Set output
        id: step1
        run: echo "result=success" >> $GITHUB_OUTPUT
      
      # Use output from another step
      - name: Get output
        run: echo "${{ steps.step1.outputs.result }}"
      
      # Add a system path
      - name: Add to PATH
        run: echo "$HOME/.local/bin" >> $GITHUB_PATH
      
      # Create an error annotation
      - name: Create annotation
        run: echo "::error file=app.js,line=10,col=15::Something went wrong"
      
      # Set a debug message
      - name: Debug message
        run: echo "::debug::This is a debug message"
      
      # Group log lines
      - name: Group logs
        run: |
          echo "::group::My group"
          echo "Inside group"
          echo "::endgroup::"
      
      # Mask a value in logs
      - name: Mask a value
        run: echo "::add-mask::sensitive-value"
```

## Common Use Cases

### Node.js Project
```yaml
name: Node.js CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Test
        run: npm test
      
      - name: Build
        run: npm run build
```

### Docker Build and Push
```yaml
name: Docker Build

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myorg/myapp
          tags: |
            type=semver,pattern={{version}}
            type=ref,event=branch
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Deploy to AWS
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Build app
        run: npm ci && npm run build
      
      - name: Deploy to S3
        run: aws s3 sync ./dist s3://my-bucket/ --delete
      
      - name: Invalidate CloudFront
        run: aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DISTRIBUTION_ID }} --paths "/*"
```

### Release Workflow
```yaml
name: Create Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build
        run: |
          npm ci
          npm run build
      
      - name: Create artifacts
        run: |
          tar -zcf release.tar.gz dist/
          zip -r release.zip dist/
      
      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref_name }}
          draft: false
          prerelease: false
      
      - name: Upload Release Assets
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./release.tar.gz
          asset_name: release.tar.gz
          asset_content_type: application/gzip
```

## Best Practices

### Security Best Practices
- Always use specific versions for actions (e.g., `actions/checkout@v4` instead of `actions/checkout@main`)
- Limit permissions to the minimum required
- Use GITHUB_TOKEN with minimum scopes needed
- Never hardcode secrets in workflow files
- Use OpenID Connect for cloud provider authentication
- Set up code scanning with CodeQL

### Performance Optimization
- Use build matrix to run tests in parallel
- Use job dependencies to optimize workflow
- Cache dependencies to speed up builds
- Use GitHub-hosted runners for standard workloads
- Use self-hosted runners for specific requirements
- Cancel in-progress workflows with concurrency groups

### Maintenance Tips
- Use composite actions to reuse common steps
- Create reusable workflows
- Document workflows with comments
- Set up workflow status badges in README
- Schedule regular maintenance workflows
- Use workflow_dispatch for manual runs and testing

## Common GitHub Context Variables

```yaml
# Common GitHub context variables
steps:
  - name: Print GitHub context
    env:
      GITHUB_CONTEXT: ${{ toJson(github) }}
    run: echo "$GITHUB_CONTEXT"
  
  - name: Common variables
    run: |
      echo "Repository: ${{ github.repository }}"
      echo "Branch: ${{ github.ref }}"
      echo "SHA: ${{ github.sha }}"
      echo "Actor: ${{ github.actor }}"
      echo "Workflow: ${{ github.workflow }}"
      echo "Event name: ${{ github.event_name }}"
      echo "Job: ${{ github.job }}"
      echo "Run number: ${{ github.run_number }}"
      echo "Run attempt: ${{ github.run_attempt }}"
```

## Environment Files

```bash
# Setting an environment variable
echo "MY_VAR=some value" >> $GITHUB_ENV

# Multiline values
echo 'MY_MULTILINE<<EOF' >> $GITHUB_ENV
echo 'line 1' >> $GITHUB_ENV
echo 'line 2' >> $GITHUB_ENV
echo 'EOF' >> $GITHUB_ENV

# Setting an output
echo "my_output=some value" >> $GITHUB_OUTPUT

# Adding to PATH
echo "$HOME/.local/bin" >> $GITHUB_PATH
```

## Expression Syntax

```yaml
# Basic expressions
steps:
  - if: ${{ github.event_name == 'push' }}
    run: echo "This is a push event"
  
  - if: ${{ contains(github.event.head_commit.message, 'release') }}
    run: echo "Release commit"
  
  - if: ${{ startsWith(github.ref, 'refs/tags/') }}
    run: echo "Tag push"
  
  - if: ${{ endsWith(github.ref, '-dev') }}
    run: echo "Development branch"
  
  - if: ${{ github.actor == 'octocat' }}
    run: echo "Action by octocat"
  
  - if: ${{ github.repository == 'octocat/Hello-World' }}
    run: echo "Hello World repo"
  
  - if: ${{ success() }}
    run: echo "Previous steps succeeded"
  
  - if: ${{ always() }}
    run: echo "Always runs"
  
  - if: ${{ failure() }}
    run: echo "A previous step failed"
  
  - if: ${{ cancelled() }}
    run: echo "Workflow was cancelled"
```

## Troubleshooting

### Common Issues and Solutions

1. **Workflow Not Triggered**
   - Check event trigger configuration
   - Verify branch/tag/path patterns
   - Check repository permissions

2. **Secrets Not Working**
   - Confirm secrets are set correctly in repository settings
   - Check if the workflow has proper permissions
   - Verify secret usage syntax

3. **Job Failures**
   - Check for syntax errors in YAML
   - View detailed logs in GitHub Actions tab
   - Check runner environment issues
   - Verify dependencies and prerequisites

4. **Debugging Tips**
   - Add debug messages: `echo "::debug::This is a debug message"`
   - Use `set -x` in bash scripts for verbose logging
   - Enable step debug logs: Set repository secrets `ACTIONS_RUNNER_DEBUG` and `ACTIONS_STEP_DEBUG` to `true`
   - Use `if: always()` to run diagnostic steps even after failures
