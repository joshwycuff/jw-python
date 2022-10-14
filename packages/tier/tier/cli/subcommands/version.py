def version():
    from tier.internal.meta import meta
    print(f'{meta.package_name} {meta.package_version}')
