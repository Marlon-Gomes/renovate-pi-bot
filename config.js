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

  // Dashboard and Lifecycle
  dependencyDashboard: true,
  rebaseWhen: 'conflicted',

  // Execution Logic
  onboarding: true, // Creates an onboarding PR for new repos
  // Use local timezone if environment variable is set, else UTC as default
  timezone: process.env.RENOVATE_TIMEZONE || 'UTC',

  // Global Settings
  extends: [
    'config:recommended' // Applies industry standard best practices
  ],
};
