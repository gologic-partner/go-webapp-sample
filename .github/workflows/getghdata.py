import requests
import json
import sys
import os

owner = os.environ.get('GITHUB_REPOSITORY').split('/',1)[0]
repo = os.environ.get('GITHUB_REPOSITORY_OWNER')
gh_token = os.environ.get('GITHUB_TOKEN')

def make_query(after_cursor=None):
    return """
query getVulnerabilitiesByRepoAndOwner($name: String!, $owner: String!) {
  repository(name: $name, owner: $owner) {
    vulnerabilityAlerts(first: 100, after:AFTER, states: OPEN) {
      nodes {
        id
        createdAt
        vulnerableManifestPath
        securityVulnerability {
          severity
          updatedAt
          package {
            name
            ecosystem
          }
          firstPatchedVersion {
            identifier
          }
          vulnerableVersionRange
          advisory {
            description
            summary
            identifiers {
              value
              type
            }
            references {
              url
            }
            cvss {
              vectorString
            }
          }
        }
        vulnerableManifestPath
        state
        vulnerableManifestFilename
        vulnerableRequirements
        number
        dependencyScope
        dismissComment
        dismissReason
        dismissedAt
        fixedAt
      }
      totalCount
      pageInfo {
        endCursor
        hasNextPage
        hasPreviousPage
        startCursor
      }
    }
    nameWithOwner
    url
  }
}
""".replace(
        "AFTER", '"{}"'.format(after_cursor) if after_cursor else "null"
    )

# accumulates all pages data into a single object
def get_dependabot_alerts_repository(repo, owner):
    keep_fetching = True
    after_cursor = None
    output_result = {"data": {"repository": {"vulnerabilityAlerts": {"nodes": []}}}}
    while keep_fetching:
        headers = {"Authorization": gh_token}

        request = requests.post(
            url="https://api.github.com/graphql",
            json={
                "operationName": "getVulnerabilitiesByRepoAndOwner",
                "query": make_query(after_cursor),
                "variables": {"name": repo, "owner": owner},
            },
            headers=headers,
        )

        result = request.json()
        output_result["data"]["repository"]["name"] = result["data"]["repository"][
            "name"
        ]
        output_result["data"]["repository"]["url"] = result["data"]["repository"]["url"]
        if result["data"]["repository"]["vulnerabilityAlerts"]["totalCount"] == 0:
            return None

        output_result["data"]["repository"]["vulnerabilityAlerts"]["nodes"] += result[
            "data"
        ]["repository"]["vulnerabilityAlerts"]["nodes"]

        keep_fetching = result["data"]["repository"]["vulnerabilityAlerts"]["pageInfo"][
            "hasNextPage"
        ]
        after_cursor = result["data"]["repository"]["vulnerabilityAlerts"]["pageInfo"][
            "endCursor"
        ]
    print(
        "Fetched {} alerts for repo {}/{}".format(
            result["data"]["repository"]["vulnerabilityAlerts"]["totalCount"],
            owner,
            repo,
        )
    )
    return json.dumps(output_result, indent=2)

print(get_dependabot_alerts_repository(owner, repo))