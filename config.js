const HOME = '/tmp/renovate'; // Renovate's internal working directory

module.exports = {
  platform: 'github',

  // Repository Discovery
  // Automatically find all repositories the bot has access to
  autodiscover: true,
  autodiscoverFilter: process.env.RENOVATE_AUTODISCOVER_FILTER || '*',

  // Use bot credentials for commit, comments, and PR authorship
  gitAuthor: process.env.RENOVATE_GIT_AUTHOR,

  // Storage and Caching
  baseDir: HOME,
  cacheDir: `${HOME}/cache`, // Specific directory for persistent data
  containerbaseDir: `${HOME}/containerbase`, // Specific directory for downloaded binaries/tools
  persistRepoData: true, // Speeds up nightly runs by keeping git clones

  extends: [
    'config:best-practices',
    ':separateMultipleMajorReleases',
    'packages:linters',
    'packages:unitTest'
  ],

  // Execution Logic
  onboarding: true, // Creates an onboarding PR for new repos
  // Use local timezone if environment variable is set, else UTC as default
  timezone: process.env.RENOVATE_TIMEZONE || 'UTC',
  // Pin deps to exact versions (override locally for libraries)
  rangeStrategy: 'pin',

  // Release Age & Stability
  minimumReleaseAge: '14 days',
  minimumReleaseAgeBehaviour: 'timestamp-optional',
  internalChecksFilter: 'strict', // Recommended for use with minimumReleaseAge

  // Lock File Maintenance
  // By default, this runs before 4am Mondays.
  lockFileMaintenance: {
    enabled: true
  },

  // Security Scanning and Prioritization
  vulnerabilityAlerts: {
    enabled: true,
  },
  osvVulnerabilityAlerts: true,

  packageRules: [
    {
      // Match all security-related updates
      matchCategories: ["security"],
      // Set limit to 0 to bypass the default 2 PR/hour limit from config
      prHourlyLimit: 0,
      // Ensures no labels are added to the PR
      addLabels: [],
      // Ensures no security labels are added to the Dashboard issue
      dependencyDashboardLabels: []
    },
    {
      // Match Python version in pyproject.toml requires-python
      matchDatasources: ["python-version"],  // Correct for requires-python/python-version
      rangeStrategy: "update-lockfile",      // Keeps your lockfile focus
      postUpgradeTasks: {
        commands: ["uv python pin {{newValue}}"],  // Pins .python-version to match requires-python
        fileFilters: [".python-version", "pyproject.toml"],  // Covers common files
        executionMode: "update-lockfile"  // Runs in artifact phase
      }
    }
  ],
  allowedCommands: [
    "^(?:\\./)?tools/[\\w-]+\\.sh.*$",          // Whitelist custom post-upgrade commands
    "^uv python pin (3\\.[0-9]+\\.[0-9]+)?$",  // Matches "uv python pin 3.14.4" or bare
  ],

  allowShellExecutorForPostUpgradeCommands: true,
  // Tool environment overrides to ensure tools have the right permissions
  customEnvVariables: {
    HOME: `${HOME}`,
    XDG_DATA_HOME: `${HOME}/.local/share`,
    XDG_CACHE_HOME: `${HOME}/cache`,  // Enables automatic discovery for UV, Go
    GOPATH: `${HOME}/cache/go`        // Required: Go doesn't use XDG_DATA_HOME
  }
};
