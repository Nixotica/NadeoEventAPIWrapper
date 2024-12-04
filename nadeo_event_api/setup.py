from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="nadeo_event_api",
        version="0.0.1",
        packages=find_packages(),
        include_package_data=True,
        package_data={
            "nadeo_event_api.objects.outbound.pastebin": ["pastebin_2v2_template.json"],
        },
    )
