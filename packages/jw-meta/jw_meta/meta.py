class Meta:

    def __init__(self, package_name: str):
        self.package_name = package_name
        self.package_version = self.get_package_version()

    def __repr__(self) -> str:
        return f'{self.package_name}-{self.package_version}'

    def get_package_version(self, default: str = '0.0.0') -> str:
        try:
            import pkg_resources

            distribution = pkg_resources.get_distribution(self.package_name)
            return distribution.version
        except:
            return default
