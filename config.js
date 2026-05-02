module.exports = {
  platform: 'github',

  // Repository Discovery
  // Automatically find all repositories the bot has access to
  autodiscover: true,
  autodiscoverFilter: process.env.RENOVATE_AUTODISCOVER_FILTER || '*',

  // Use bot credentials for commit, comments, and PR authorship
  gitAuthor: process.env.RENOVATE_GIT_AUTHOR,

  // Storage and Caching
  baseDir: '/tmp/renovate', // Renovate's internal working directory
  cacheDir: '/tmp/renovate/cache', // Specific directory for persistent data
  containerbaseDir: '/tmp/renovate/containerbase', // Specific directory for downloaded binaries/tools
  persistRepoData: true, // Speeds up nightly runs by keeping git clones

  // Global Settings
  extends: [
    'config:recommended' // Applies industry standard best practices
  ],

  // Dashboard and Lifecycle
  dependencyDashboard: true,
  rebaseWhen: 'conflicted',

  // Execution Logic
  onboarding: true, // Creates an onboarding PR for new repos
  // Use local timezone if environment variable is set, else UTC as default
  timezone: process.env.RENOVATE_TIMEZONE || 'UTC',

  // Security Scanning and Prioritization
  osvVulnerabilityAlerts: true,
  vulnerabilityAlerts: {
    enabled: true,
    branchTopic: "{{depNameSanitized}}-{{newMajor}}.x",
    commitMessageSuffix: ""
  },

  packageRules: [
    {
      // Match all security-related updates
      matchUpdateTypes: ["security"],
      // Set limit to 0 to bypass the default 2 PR/hour limit from config
      prHourlyLimit: 0,
      // Ensures no labels are added to the PR
      addLabels: [],
      // Ensures no security labels are added to the Dashboard issue
      dependencyDashboardLabels: [],
      // Enable silent patching
      automerge: true,
      automergeType: "pr", // Creates PR then merges it
      automergeStrategy: "squash",
      // By-pass the need for a passing status check
      // WARNING: Repos with status checks should enable them in their own renovate.json
      requiredStatusChecks: [],
    }
  ],
  allowedCommands: ["^(?:\\./)?tools/[\\w-]+\\.sh.*$"],
  allowShellExecutorForPostUpgradeCommands: true,
  // Go override to ensure go tools have the right permissions
  customEnvVariables: {
    GOCACHE: '/tmp/renovate/cache/go-build',
    GOPATH: '/tmp/renovate/cache/go',
    HOME: '/tmp/renovate', // Keeps tools out of /home/ubuntu
  }
};
