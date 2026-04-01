from beaker_kernel.lib.integrations.adhoc import AdhocIntegrationProvider, AdhocSpecificationIntegration

class BiomeAdhocIntegrations(AdhocIntegrationProvider):
    display_name="Biome Specialist Agents"
    slug="biome"

    @property
    def prompt(self):
        agent_details = {spec.slug: spec.description for spec in self.specifications}
        delimiter = "```"
        parts = [
            self.prompt_instructions if self.prompt_instructions else "",
            ""
            f"{self.display_name}:",
            "You have access to the following integrations. Use `load_integration_docs` to load an integration's",
            "full documentation directly into your context when you need to work with it.",
            "",
            delimiter
        ]
        parts.extend([f"Integration: {slug}\nDescription: {desc}\n\n" for slug, desc in agent_details.items()])
        parts.append(delimiter)
        return "\n".join(parts)
