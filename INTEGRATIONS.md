# Platform Integrations Guide

This document explains how to set up and configure platform integrations for your Profile as Code automation.

## Overview

The integration system allows you to automatically post announcements to various platforms when your profile updates. Each integration is:
- **Configurable** via `profile.json`
- **Extensible** - easy to add new platforms
- **Secure** - uses GitHub Secrets for API tokens

## Available Integrations

### 1. LinkedIn Integration

Posts announcements to your LinkedIn feed when profile updates.

**Capabilities:**
- ✅ Create posts/shares announcing profile updates
- ❌ Cannot update LinkedIn profile directly (API limitation)
- ❌ Cannot update Experience/Skills sections (API limitation)

**Setup Steps:**

#### Step 1: Get LinkedIn Access Token

**Option A: Production (Real LinkedIn Posts)**

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Create a new app
3. Request access to the "Share on LinkedIn" product
4. Get OAuth 2.0 credentials
5. Obtain an access token with `w_member_social` scope

For detailed OAuth flow, see: https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication

**Option B: Dry-Run Mode (Testing)**

Use the token `dry-run` to simulate posts without actually posting to LinkedIn:

```bash
# Local testing
LINKEDIN_ACCESS_TOKEN=dry-run uv run main.py run-integrations
```

#### Step 2: Add GitHub Secret

1. Go to your repository: `https://github.com/YOUR_USERNAME/YOUR_USERNAME`
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `LINKEDIN_ACCESS_TOKEN`
5. Value: Your access token (or `dry-run` for testing)
6. Click **Add secret**

#### Step 3: Configure in profile.json

Enable the integration in your `profile.json`:

```json
{
  "integrations": {
    "linkedin": {
      "enabled": true,
      "postOnUpdate": true,
      "postTemplate": "🎉 ¡Acabo de actualizar mi perfil profesional!\n\nVisita https://github.com/{github} para ver mis últimos proyectos.\n\n#OpenToWork #SoftwareEngineering"
    }
  }
}
```

**Configuration Options:**
- `enabled` (boolean): Enable/disable the integration
- `postOnUpdate` (boolean): Auto-post when profile updates
- `postTemplate` (string, optional): Custom post template
  - Available variables: `{name}`, `{github}`, `{version}`

#### Step 4: Test Locally

```bash
# With dry-run mode
LINKEDIN_ACCESS_TOKEN=dry-run uv run main.py run-integrations

# With real token (will actually post!)
LINKEDIN_ACCESS_TOKEN=your_token_here uv run main.py run-integrations
```

#### Step 5: Commit and Push

Once configured, the GitHub Actions workflow will automatically run integrations when you update `profile.json`:

```bash
git add profile.json
git commit -m "feat: enable LinkedIn integration"
git push
```

The workflow will:
1. Validate profile.json
2. Generate README
3. **Run integrations** (post to LinkedIn)
4. Commit changes

## Adding New Integrations

Want to add Twitter, Dev.to, or another platform? Follow this pattern:

### 1. Create Integration Class

Create `scripts/integrations/platform_name.py`:

```python
from scripts.integrations.base import BaseIntegration

class PlatformNameIntegration(BaseIntegration):
    def validate_config(self) -> bool:
        # Check if API token exists and config is valid
        pass

    def execute(self) -> dict:
        # Post update to platform
        pass

# Auto-register
from scripts.integrations.registry import IntegrationRegistry
IntegrationRegistry.register('platform_name', PlatformNameIntegration)
```

### 2. Import in main.py

Add to `main.py`:

```python
import scripts.integrations.platform_name  # noqa: F401
```

### 3. Configure in profile.json

```json
{
  "integrations": {
    "platform_name": {
      "enabled": true,
      "option1": "value"
    }
  }
}
```

### 4. Add GitHub Secret (if needed)

Add `PLATFORM_NAME_API_TOKEN` to GitHub Secrets.

### 5. Update Workflow (if needed)

Add environment variable to `.github/workflows/profile-automation.yml`:

```yaml
env:
  LINKEDIN_ACCESS_TOKEN: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
  PLATFORM_NAME_API_TOKEN: ${{ secrets.PLATFORM_NAME_API_TOKEN }}
```

## Troubleshooting

### Integration not running

Check:
- [ ] Integration is `enabled: true` in profile.json
- [ ] GitHub Secret is set correctly
- [ ] Token has required permissions/scopes

### Dry-run mode

To test without actually posting:

```bash
LINKEDIN_ACCESS_TOKEN=dry-run uv run main.py run-integrations
```

This will simulate the post and show what would be posted.

### View integration logs

Check GitHub Actions workflow logs:
1. Go to **Actions** tab in your repository
2. Click on the latest workflow run
3. Expand **Run Platform Integrations** job
4. View detailed logs

## Security Notes

- **Never commit API tokens** to the repository
- Always use GitHub Secrets for sensitive tokens
- Tokens are only accessible in GitHub Actions environment
- Local development can use `.env` file (add to `.gitignore`)

## Future Integration Ideas

Easy to add:
- **Twitter/X**: Auto-tweet profile updates
- **Dev.to**: Sync projects as blog posts
- **Hashnode**: Cross-post technical content
- **Medium**: Share articles
- **Slack/Discord**: Notify team channels
- **Email**: Send update notifications

Each integration follows the same pattern - extend `BaseIntegration` and register!
