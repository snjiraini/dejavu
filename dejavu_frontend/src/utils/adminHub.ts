/**
 * AdminHub functionality for the Dejavu frontend
 */

// Toggle sidebar visibility
export const toggleSidebar = (sidebarId: string = "sidebar"): void => {
  const sidebar = document.getElementById(sidebarId);
  if (sidebar) {
    sidebar.classList.toggle("hide");
  }
};

// Adjust sidebar based on screen size
export const adjustSidebar = (sidebarId: string = "sidebar"): void => {
  const sidebar = document.getElementById(sidebarId);
  if (!sidebar) return;

  if (window.innerWidth <= 576) {
    sidebar.classList.add("hide");
    sidebar.classList.remove("show");
  } else {
    sidebar.classList.remove("hide");
    sidebar.classList.add("show");
  }
};

// Toggle dark mode
export const toggleDarkMode = (): void => {
  document.body.classList.toggle("dark");

  // Save dark mode preference to localStorage
  const isDarkMode = document.body.classList.contains("dark");
  localStorage.setItem("darkMode", isDarkMode ? "true" : "false");
};

// Toggle notification menu
export const toggleNotificationMenu = (): void => {
  const notificationMenu = document.querySelector(".notification-menu");
  const profileMenu = document.querySelector(".profile-menu");

  if (notificationMenu) {
    notificationMenu.classList.toggle("show");
  }

  if (profileMenu && profileMenu.classList.contains("show")) {
    profileMenu.classList.remove("show");
  }
};

// Toggle profile menu
export const toggleProfileMenu = (): void => {
  const profileMenu = document.querySelector(".profile-menu");
  const notificationMenu = document.querySelector(".notification-menu");

  if (profileMenu) {
    profileMenu.classList.toggle("show");
  }

  if (notificationMenu && notificationMenu.classList.contains("show")) {
    notificationMenu.classList.remove("show");
  }
};

// Close menus when clicked outside
export const setupOutsideClickHandler = (): void => {
  window.addEventListener("click", (e) => {
    const target = e.target as HTMLElement;
    const notificationMenu = document.querySelector(".notification-menu");
    const profileMenu = document.querySelector(".profile-menu");

    if (!target.closest(".notification") && !target.closest(".profile")) {
      if (notificationMenu) {
        notificationMenu.classList.remove("show");
      }

      if (profileMenu) {
        profileMenu.classList.remove("show");
      }
    }
  });
};

// Initialize dark mode based on saved preference
export const initDarkMode = (): void => {
  const savedDarkMode = localStorage.getItem("darkMode") === "true";
  if (savedDarkMode) {
    document.body.classList.add("dark");
  } else {
    document.body.classList.remove("dark");
  }
};

// Initialize AdminHub functionality
export const initAdminHub = (): void => {
  window.addEventListener("load", () => {
    adjustSidebar();
    initDarkMode();
  });
  window.addEventListener("resize", () => adjustSidebar());

  // Setup menu handlers
  setupOutsideClickHandler();

  // Setup dark mode toggle
  const switchMode = document.getElementById("switch-mode");
  if (switchMode) {
    switchMode.addEventListener("change", toggleDarkMode);
  }
};
