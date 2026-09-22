# Notify · Slack

Posts a colour-coded status message with a "View run" button to Slack through an **incoming webhook**.

## Usage: summary at the end of a pipeline

```yaml
jobs:
  notify:
    if: always()
    needs: [build, deploy_prod]
    permissions:
      contents: read
    uses: utrains/ci-cd-pipeline-templates/.github/workflows/notify-slack.yml@v2
    with:
      status: ${{ contains(needs.*.result, 'failure') && 'failure' || contains(needs.*.result, 'cancelled') && 'cancelled' || 'success' }}
      message: "Deployed `${{ github.ref_name }}` to production."
    secrets:
      slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## Notes

- **Breaking change from v1:** this replaces `slack-team-notifica.yml`. The webhook is now a **secret** named
  `slack_webhook_url`. The old `webhook_url` input exposed it in logs.
- Create the webhook under Slack **Apps → Incoming Webhooks**. Each webhook posts to one channel.
- The payload is built with `jq`, so quotes and newlines in `message` are safe.

<!-- BEGIN GENERATED REFERENCE: do not edit, run scripts/generate_docs.py -->

## Reference

**Workflow file:** [`notify-slack.yml`](../../.github/workflows/notify-slack.yml)

### Permissions the calling job must grant

```yaml
permissions:
  contents: read
```

### Inputs

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `status` | string | no | `info` | success \| failure \| cancelled \| info — typically computed from needs.*.result. |
| `title` | string | no |  | Message title. Empty = "<repo> · <workflow>". |
| `message` | string | no |  | Message body (Slack mrkdwn). |
| `include_run_link` | boolean | no | `true` | Add a 'View run' button linking to this workflow run. |
| `runs_on` | string | no | `ubuntu-latest` | Runner label, or a JSON array of labels. |

### Secrets

| Name | Required | Description |
|---|---|---|
| `slack_webhook_url` | yes | Slack incoming-webhook URL. |

<!-- END GENERATED REFERENCE -->
