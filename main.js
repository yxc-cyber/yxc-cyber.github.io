const navLinks = Array.from(document.querySelectorAll(".dock-nav a"));
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);
const backgroundLayer = document.querySelector(".page-background");
const backgroundImage = new Image();
backgroundImage.src = "assets/bg-contours.svg";

let ticking = false;
let maxScroll = 0;
let backgroundTravel = 0;
let backgroundAspectRatio = 1440 / 960;
let sectionStops = [];
let activeId = null;

function scrollOffset() {
  const styles = window.getComputedStyle(document.documentElement);
  const dockHeight = Number.parseFloat(styles.getPropertyValue("--dock-height")) || 0;
  const jumpClearance = Number.parseFloat(styles.getPropertyValue("--jump-clearance")) || 0;
  return dockHeight + jumpClearance;
}

function measureSections() {
  const offset = scrollOffset();
  sectionStops = sections.map((section) => ({
    id: section.id,
    top: Math.max(0, section.offsetTop - offset),
    bottom: section.offsetTop + section.offsetHeight,
  }));
}

function updateBackgroundMetrics() {
  maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);

  if (backgroundImage.naturalWidth && backgroundImage.naturalHeight) {
    backgroundAspectRatio = backgroundImage.naturalWidth / backgroundImage.naturalHeight;
  }

  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;
  const parallaxRate = 0.45;
  const minTravel = maxScroll * parallaxRate;
  const minLayerHeight = viewportHeight + minTravel;
  let layerWidth = viewportWidth;
  let layerHeight = layerWidth / backgroundAspectRatio;

  if (layerHeight < minLayerHeight) {
    layerHeight = minLayerHeight;
    layerWidth = layerHeight * backgroundAspectRatio;
  }

  backgroundTravel = Math.max(0, layerHeight - viewportHeight);

  if (backgroundLayer) {
    backgroundLayer.style.width = `${Math.ceil(layerWidth)}px`;
    backgroundLayer.style.height = `${Math.ceil(layerHeight)}px`;
  }
}

function setBackgroundParallax() {
  if (!backgroundLayer) {
    return;
  }

  const progress = maxScroll > 0 ? window.scrollY / maxScroll : 0;
  const y = backgroundTravel * progress * -1;
  backgroundLayer.style.transform = `translate3d(-50%, ${y}px, 0)`;
}

function setActiveNav() {
  const pageBottom = window.scrollY + window.innerHeight;
  const documentBottom = document.documentElement.scrollHeight - 2;
  const anchor = window.scrollY + 1;
  let nextActiveId = sectionStops[0]?.id;

  if (pageBottom >= documentBottom) {
    nextActiveId = sectionStops[sectionStops.length - 1]?.id;
  } else for (const section of sectionStops) {
    if (section.top <= anchor) {
      nextActiveId = section.id;
    }
  }

  if (nextActiveId === activeId) {
    return;
  }

  activeId = nextActiveId;
  navLinks.forEach((link) => {
    link.classList.toggle("is-active", link.getAttribute("href") === `#${activeId}`);
  });
}

function updateMeasurements() {
  measureSections();
  updateBackgroundMetrics();
}

function updateOnScroll() {
  setActiveNav();
  setBackgroundParallax();
  ticking = false;
}

function requestScrollUpdate() {
  if (ticking) {
    return;
  }

  ticking = true;
  window.requestAnimationFrame(updateOnScroll);
}

function refreshLayout() {
  updateMeasurements();
  requestScrollUpdate();
}

updateMeasurements();
updateOnScroll();
window.addEventListener("scroll", requestScrollUpdate, { passive: true });
window.addEventListener("resize", refreshLayout);
window.addEventListener("load", refreshLayout);
backgroundImage.addEventListener("load", refreshLayout);
navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    link.blur();
  });
});
