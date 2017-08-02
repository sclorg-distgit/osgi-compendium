%{?scl:%scl_package osgi-compendium}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}osgi-compendium
Version:        6.0.0
Release:        3.1%{?dist}
Summary:        Interfaces and Classes for use in compiling OSGi bundles
License:        ASL 2.0
URL:            http://www.osgi.org
BuildArch:      noarch

Source0:        https://osgi.org/download/r6/osgi.cmpn-%{version}.jar

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(javax.persistence:persistence-api)
BuildRequires:  %{?scl_prefix}mvn(javax.servlet:javax.servlet-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.osgi:osgi.annotation)
BuildRequires:  %{?scl_prefix}mvn(org.osgi:osgi.core)

%description
OSGi Compendium, Interfaces and Classes for use in compiling bundles.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
This package provides %{summary}.

%prep
%setup -n %{pkg_name}-%{version} -q -c

rm -r org
find -name '*.class' -delete

mkdir -p src/main/{java,resources}
mv OSGI-OPT/src/org src/main/java/
mv xmlns src/main/resources

# J2ME stuff
rm -r src/main/java/org/osgi/service/io

mv META-INF/maven/org.osgi/osgi.cmpn/pom.xml .

%pom_xpath_inject pom:project '
<packaging>bundle</packaging>
<properties>
  <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <extensions>true</extensions>
      <configuration>
        <instructions>
          <Bundle-Name>${project.artifactId}</Bundle-Name>
          <Bundle-SymbolicName>${project.artifactId}</Bundle-SymbolicName>
        </instructions>
      </configuration>
    </plugin>
  </plugins>
</build>'

%pom_add_dep org.osgi:osgi.annotation::provided
%pom_add_dep org.osgi:osgi.core::provided
%pom_add_dep javax.servlet:javax.servlet-api::provided
%pom_add_dep javax.persistence:persistence-api::provided

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc about.html

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 6.0.0-3.1
- Automated package import and SCL-ization

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 10 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.0.0-2
- Fix scopes of injected Maven dependencies

* Mon Oct 12 2015 Michael Simacek <msimacek@redhat.com> - 6.0.0-1
- Initial packaging
