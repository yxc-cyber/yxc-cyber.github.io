const navLinks = Array.from(document.querySelectorAll(".dock-nav a"));
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);
const backgroundLayer = document.querySelector(".page-background");
const backgroundImage = new Image();
backgroundImage.src = "assets/bg-contours.svg";
const solidNames = Array.from(document.querySelectorAll(".solid-name"));
const heroIconRows = Array.from(document.querySelectorAll(".hero-icons"));

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
  fitHeroContent();
}

function fitSolidNames() {
  solidNames.forEach((name) => {
    const clip = name.closest(".name-clip");
    if (!clip) {
      return;
    }

    name.style.fontSize = "";
    const styles = window.getComputedStyle(name);
    const baseSize = Number.parseFloat(styles.fontSize);
    const left = Number.parseFloat(styles.left) || 0;
    const available = Math.max(120, clip.clientWidth - left - 22);

    if (!baseSize || name.scrollWidth <= available) {
      return;
    }

    const nextSize = Math.max(22, Math.floor(baseSize * (available / name.scrollWidth)));
    name.style.fontSize = `${nextSize}px`;
  });
}

function fitHeroStars() {
  heroIconRows.forEach((row) => {
    const stars = Array.from(row.querySelectorAll(".hero-stars img"));
    stars.forEach((star) => star.classList.remove("is-hidden"));

    const copyRect = row.closest(".hero-copy")?.getBoundingClientRect();
    const barRect = row.closest(".hero-bar")?.getBoundingClientRect();
    const containerRect = copyRect && copyRect.width > 0 ? copyRect : barRect;
    const rowRect = row.getBoundingClientRect();
    const available = containerRect
      ? Math.max(0, containerRect.right - rowRect.left - 22)
      : row.clientWidth;

    for (let index = stars.length - 1; index >= 0 && row.scrollWidth > available; index -= 1) {
      stars[index].classList.add("is-hidden");
    }
  });
}

function syncHeroSeparatorGaps() {
  solidNames.forEach((name) => {
    const copy = name.closest(".hero-copy");
    const clip = name.closest(".name-clip");
    const iconRow = copy?.querySelector(".hero-icons");

    if (!copy || !clip || !iconRow) {
      return;
    }

    iconRow.style.removeProperty("--solid-separator-margin");

    const nameRect = name.getBoundingClientRect();
    const clipRect = clip.getBoundingClientRect();
    const iconAfterStyles = window.getComputedStyle(iconRow, "::after");
    const copyStyles = window.getComputedStyle(copy);
    const separatorTop = Number.parseFloat(iconAfterStyles.top) || 0;
    const desiredGap = Number.parseFloat(copyStyles.getPropertyValue("--solid-separator-gap")) || 14;
    const nameBottomInClip = nameRect.bottom - clipRect.top;
    const nextMargin = nameBottomInClip + desiredGap - clip.clientHeight - separatorTop;

    iconRow.style.setProperty("--solid-separator-margin", `${Math.max(0, Math.round(nextMargin))}px`);
  });
}

function fitHeroContent() {
  fitSolidNames();
  syncHeroSeparatorGaps();
  fitHeroStars();
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
