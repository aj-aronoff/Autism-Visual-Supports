# Resources doc — every link, verified 3 November 2026

Split out of `RESOURCES-AND-CRITERIA-NOV-2.md` §6.4 on 7 November 2026, so that file stays
an analysis of the criteria rather than a URL index. The findings — no drift, two dead
links, the provenance warning — stay there. This is the evidence behind them.

**How these were checked, because the obvious method does not work.**
`success.outsystems.com` is a single-page app that returns **HTTP 200 for any path**, so a
status code proves nothing. Each link was matched against the site's own sitemap (4,502
URLs, from the address `robots.txt` points to) **with a deliberately bogus path as a
control** — absent, as it should be. The YouTube ids went through oEmbed, which 404s on a
dead id.

**23 of the 27 carry `?utm_source=chatgpt.com`**, so the document was assembled with
ChatGPT's help and not fully proofed — which is how a plausible path that was never real
got in. Treat it as a reading list to verify, not an index.

Paths are relative to `https://success.outsystems.com/documentation/`; `utm_source`
stripped.

| Anchor text in the doc | Path | Verdict |
|---|---|---|
| Agentic Apps section in the ODC | `outsystems_developer_cloud/building_apps/build_ai_powered_apps/agentic_apps_in_odc/` | in sitemap |
| YouTube playlist | `https://www.youtube.com/watch?v=2JtGN6OCfjs&list=PLxALhSwsaivy1afIHT5TElTJJs9OMHNcX&utm_source=chatgpt.com` | live (oEmbed title matches) |
| official Mentor documentation | `outsystems_developer_cloud/agentic_development/mentor/` | in sitemap |
| OutSystems MCP documentation | `outsystems_developer_cloud/agentic_development/outsystems_mcp/` | in sitemap |
| Integration with External Systems | `outsystems_developer_cloud/integration_with_external_systems/` | in sitemap |
| Integrate with External Data Sources Using Data Fabric | `outsystems_developer_cloud/integration_with_external_systems/integrate_with_external_data_sources_using_data_fabric/` | in sitemap |
| Integrating OutSystems with Your Ecosystem | `11/integration_with_external_systems/integrating_outsystems_with_your_ecosystem/` | in sitemap |
| Configure a Private Gateway | `outsystems_developer_cloud/managing_outsystems_platform_and_apps/configure_a_private_gateway_to_your_network/` | in sitemap |
| Cloud-Native Architecture of ODC | `outsystems_developer_cloud/managing_outsystems_platform_and_apps/cloud_native_architecture_of_outsystems_developer_cloud/` | in sitemap |
| Knowledge Base Integration | `outsystems_developer_cloud/building_apps/build_ai_powered_apps/agentic_apps_in_odc/knowledge_bases_in_odc/` | in sitemap |
| Semantic Search Utilization | `outsystems_developer_cloud/building_apps/build_ai_powered_apps/agentic_apps_in_odc/semantic_search_in_odc_apps/` | in sitemap |
| App Architecture (ODC) | `outsystems_developer_cloud/app_architecture/` | in sitemap |
| Reuse Elements Across Apps | `outsystems_developer_cloud/app_architecture/reuse_elements_across_apps/` | in sitemap |
| Libraries (ODC) | `outsystems_developer_cloud/libraries/` | **DEAD -> see correction below** |
| The Architecture Canvas (O11) | `11/app_architecture/designing_the_architecture_of_your_outsystems_applications/the_architecture_canvas/` | in sitemap |
| OutSystems Forge | `https://www.outsystems.com/forge/` | **NOT in sitemap** |
| Install or Update a Forge Asset | `outsystems_developer_cloud/forge/install_or_update_a_forge_asset/` | **DEAD -> see correction below** |
| Agentic Apps in ODC | `outsystems_developer_cloud/building_apps/build_ai_powered_apps/agentic_apps_in_odc/` | in sitemap |
| Agent Workbench: Agent Orchestration, workflows and humans | `https://www.youtube.com/watch?v=SUXE7NldKzg&list=PLxALhSwsaivy1afIHT5TElTJJs9OMHNcX&index=5` | live (oEmbed title matches) |
| Agent Guardrails | `outsystems_developer_cloud/building_apps/build_ai_powered_apps/agentic_apps_in_odc/agent_guardrails/` | in sitemap |
| AI Governance with OutSystems: Protect your Agents with Guardrails | `https://www.youtube.com/watch?v=ckoaRbIl8Eg` | live (oEmbed title matches) |
| Workflows in ODC | `outsystems_developer_cloud/building_apps/about_business_processes/workflows_in_odc/` | in sitemap |
| Agent Evaluations | `outsystems_developer_cloud/building_apps/build_ai_powered_apps/agentic_apps_in_odc/agent_evaluations/` | in sitemap |
| Monitoring and Troubleshooting Apps | `outsystems_developer_cloud/monitoring_and_troubleshooting_apps/` | in sitemap |
| Streaming Observability Data | `outsystems_developer_cloud/monitoring_and_troubleshooting_apps/streaming_observability_data/` | in sitemap |
| Security of OutSystems Developer Cloud | `outsystems_developer_cloud/security_of_outsystems_developer_cloud/` | in sitemap |
| Audit Trail | `outsystems_developer_cloud/monitoring_and_troubleshooting_apps/audit_trail/` | in sitemap |

## The two dead links

| Dead link, as the doc has it | The page that actually exists |
|---|---|
| `outsystems_developer_cloud/libraries/` | `outsystems_developer_cloud/building_apps/libraries/` — plus `.../libraries/use_public_elements/` |
| `outsystems_developer_cloud/forge/install_or_update_a_forge_asset/` | `outsystems_developer_cloud/building_apps/forge/install_or_update_a_forge_asset/` |

**The Libraries one matters**: ODC Libraries is what §1.2 identifies as the requirement
behind *Logic Isolation* in the Modular Architecture bucket, so the organisers' own
pointer to a scored feature 404s. Use the corrected path.
