# Step 5 GitHub Actions Setup

Create these GitHub settings before expecting the app pipeline to push images and update GitOps.

## Repository variables

In `testoranit/healthcare-ai-agent-service`, add:

```text
AWS_ACCOUNT_ID = 021655150740
AWS_REGION = ap-south-1
```

## Repository secret

In `testoranit/healthcare-ai-agent-service`, add:

```text
GITOPS_TOKEN = <fine-grained GitHub token with contents read/write on healthcare-ai-platform-gitops>
```

The default `GITHUB_TOKEN` cannot push to a separate repository, so the app pipeline needs this token to update the GitOps repo.

## Required AWS resource

The app workflow pushes to this ECR repo:

```text
021655150740.dkr.ecr.ap-south-1.amazonaws.com/healthcare-ai-dev-agent
```

That ECR repository is created by the Step 3 Terraform `ecr` module for the dev environment.
