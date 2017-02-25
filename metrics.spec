%{?_javapackages_macros:%_javapackages_macros}

Name:          metrics
Version:       3.1.2
Release:       1
Summary:       Java library which gives you what your code does in production
License:       ASL 2.0
Group:         Development/Java
URL:           http://metrics.dropwizard.io
Source0:       https://github.com/dropwizard/metrics/archive/v%{version}/%{name}-%{version}.tar.gz
# Add rabbitmq-java-client 3.5.x support
Patch0:        metrics-3.1.2-amqp-client35.patch
# Use ehcache-core instead of net.sf.ehcache:ehcache:2.8.3
Patch1:        metrics-3.1.2-ehcache-core.patch

BuildRequires: maven-local
BuildRequires: mvn(ch.qos.logback:logback-classic)
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires: mvn(com.google.guava:guava)
#BuildRequires: mvn(com.rabbitmq:amqp-client)
#BuildRequires: mvn(com.sun.jersey:jersey-server:1)
#BuildRequires: mvn(info.ganglia.gmetric4j:gmetric4j)
BuildRequires: mvn(javax.servlet:javax.servlet-api)
#BuildRequires: mvn(javax.ws.rs:javax.ws.rs-api)
BuildRequires: mvn(log4j:log4j)
BuildRequires: mvn(net.sf.ehcache:ehcache-core)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
#BuildRequires: httpcomponents-asyncclient #mvn(org.apache.httpcomponents:httpasyncclient)
BuildRequires: mvn(org.apache.httpcomponents:httpclient)
#BuildRequires: mvn(org.apache.logging.log4j:log4j-api)
#BuildRequires: mvn(org.apache.logging.log4j:log4j-core)
BuildRequires: mvn(org.apache.maven.plugins:maven-release-plugin)
#BuildRequires: mvn(org.glassfish.jersey.core:jersey-server)
#BuildRequires: mvn(org.jdbi:jdbi)
#BuildRequires: mvn(org.openjdk.jmh:jmh-core)
#BuildRequires: mvn(org.openjdk.jmh:jmh-generator-annprocess)
BuildRequires: mvn(org.slf4j:slf4j-api)

%if 0
# metrics-jetty8
BuildRequires: mvn(org.eclipse.jetty:jetty-server:8.1.11.v20130520)
# metrics-jetty9
BuildRequires: mvn(org.eclipse.jetty:jetty-client:9.2.2.v20140723)
BuildRequires: mvn(org.eclipse.jetty:jetty-server:9.2.2.v20140723)
# metrics-jetty9-legacy
BuildRequires: mvn(org.eclipse.jetty:jetty-server:9.0.4.v20130625)
BuildRequires: mvn(org.eclipse.jetty:jetty-client:9.0.4.v20130625)
# Test deps
BuildRequires: mvn(com.sun.jersey.jersey-test-framework:jersey-test-framework-inmemory)
BuildRequires: mvn(org.glassfish.jersey.test-framework.providers:jersey-test-framework-provider-inmemory)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.assertj:assertj-core:jar:1.6.1)
BuildRequires: mvn(org.eclipse.jetty:jetty-servlet)
BuildRequires: mvn(org.mockito:mockito-all)
BuildRequires: mvn(org.python:jython-standalone)
BuildRequires: mvn(org.slf4j:slf4j-simple)
%endif

# Docs deps
BuildRequires: python-sphinx
BuildRequires: texlive

BuildArch:     noarch

%description
Metrics is a Java library which gives you unparalleled insight
into what your code does in production.

Developed by Yammer to instrument their JVM-based back-end services,
Metrics provides a powerful toolkit of ways to measure the behavior
of critical components in your production environment.

With modules for common libraries like Jetty, Logback, Log4j,
Apache HttpClient, Ehcache, JDBI, Jersey and reporting back-ends like
Ganglia and Graphite, Metrics provides you with full-stack visibility.

For more information, please see the documentation.

This package provides the Metrics Core Library.


%package parent
Summary:       Metrics Parent POM

%description parent
This package provides Metrics Parent POM.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%package doc
Summary:       Metrics's user manual

%description doc
This package contains %{name}'s user manual.

%prep
%setup -q -n %{name}-%{version}
# Cleanup
find . -name "*.class" -delete
find . -name "*.jar" -type f -delete

%patch0 -p1
%patch1 -p1

# Unavailable build deps:
# see rhbz#861502#c3 rhbz#861502#c5 disable jetty9 sub-module (use jetty 9.0.4.v20130625)
#pom_disable_module metrics-jetty8
#pom_disable_module metrics-jetty9
#pom_disable_module metrics-jetty9-legacy


%pom_disable_module metrics-annotation
%pom_disable_module metrics-benchmarks
#pom_disable_module metrics-core
%pom_disable_module metrics-healthchecks
%pom_disable_module metrics-ehcache
%pom_disable_module metrics-ganglia
%pom_disable_module metrics-graphite
%pom_disable_module metrics-httpclient
%pom_disable_module metrics-httpasyncclient
%pom_disable_module metrics-jdbi
%pom_disable_module metrics-jersey
%pom_disable_module metrics-jersey2
%pom_disable_module metrics-jetty8
%pom_disable_module metrics-jetty9
%pom_disable_module metrics-jetty9-legacy
%pom_disable_module metrics-json
%pom_disable_module metrics-jvm
%pom_disable_module metrics-log4j
%pom_disable_module metrics-log4j2
%pom_disable_module metrics-logback
%pom_disable_module metrics-servlet
%pom_disable_module metrics-servlets

%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
#pom_remove_plugin -r :maven-shade-plugin

# Disable javadoc jar
%pom_xpath_remove "pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"
# Disable source jar
%pom_remove_plugin :maven-source-plugin

%pom_xpath_set "pom:properties/pom:jersey.version" 1 %{name}-jersey
%pom_add_dep javax.ws.rs:javax.ws.rs-api metrics-jersey2
sed -i "s|jersey.repackaged.||" \
 metrics-jersey2/src/main/java/com/codahale/metrics/jersey2/InstrumentedResourceMethodApplicationListener.java
%pom_add_dep com.google.guava:guava metrics-jersey2

# org.assertj:assertj-core:1.6.1 *
%pom_remove_dep -r org.assertj:assertj-core

%if 0
%mvn_package ":%{name}-jetty8" %{name}-jetty
%mvn_package ":%{name}-jetty9" %{name}-jetty
%mvn_package ":%{name}-jetty9-legacy" %{name}-jetty
%endif

%mvn_alias io.dropwizard.metrics: com.codahale.metrics:

%build

# Unavailable test dep *
%mvn_build -s -f

(
  cd docs
%if 0
  make %{?_smp_mflags} latexpdf
%endif
  make %{?_smp_mflags} singlehtml
  make %{?_smp_mflags} man
)

%install
%mvn_install

mkdir -p %{buildroot}%{_mandir}/man1
install -pm 644 docs/target/man/%{name}.1 %{buildroot}%{_mandir}/man1/

rm -rf docs/target/singlehtml/.buildinfo

%files  -f .mfiles-%{name}-core
%doc README.md
%doc LICENSE NOTICE

%files parent -f .mfiles-%{name}-parent
%doc LICENSE NOTICE


%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%files doc
%{_mandir}/man1/%{name}.*
%doc LICENSE NOTICE
%doc docs/target/singlehtml
%if 0
%doc docs/target/latex/*.pdf
%endif

%changelog
* Mon Feb 22 2016 gil cattaneo <puntogil@libero.it> - 3.1.2-3
- rebuilt

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 31 2015 gil cattaneo <puntogil@libero.it> 3.1.2-1
- update to 3.1.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 gil cattaneo <puntogil@libero.it> 3.0.1-5
- rebuilt with jersey 1.19

* Tue Feb 10 2015 gil cattaneo <puntogil@libero.it> 3.0.1-4
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 3.0.1-2
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 gil cattaneo <puntogil@libero.it> 3.0.1-1
- update to 3.0.1

* Fri Sep 28 2012 gil cattaneo <puntogil@libero.it> 2.1.3-1
- initial rpm
