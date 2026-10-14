# Mobile

Verify on a simulator or emulator that this run starts and owns.

## Launch

- Build the app with the project's own scheme or variant. Install it on a
  simulator or emulator that this run boots. Record the device ID in the `up`
  state file.
- Point the app at a local backend through build configuration or launch
  arguments. On the iOS simulator, `localhost` reaches the host machine. On the
  Android emulator, the host is `10.0.2.2`.
- Ready means the app reaches a signed-in screen with a local test identity.

## Drive

- **Scripted flows.** Use the platform UI test framework (XCUITest or
  Espresso), or a cross-platform runner such as Maestro or Appium.
- **Agent exploration.** Use simulator control tools that tap, swipe, type, and
  take screenshots.
- **Locators.** Prefer accessibility identifiers over screen coordinates.
- **Deep links.** Use them to reach a deep screen directly, but also cover the
  navigation path a user takes at least once.

## Gotchas

- Permission dialogs, onboarding screens, and update prompts block flows.
  Reset them by reinstalling the app, or pre-grant permissions with launch
  arguments.
- A real device is a different target. Simulator evidence doesn't cover
  device-only behavior such as push notifications, the camera, or performance.
