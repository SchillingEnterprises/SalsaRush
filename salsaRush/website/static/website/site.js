/** Accessible, dependency-free mobile navigation. */
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".menu-toggle");
  const navigation = document.querySelector("#primary-nav");
  if (!button || !navigation) return;
  button.addEventListener("click", () => {
    const expanded = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!expanded));
    navigation.classList.toggle("is-open", !expanded);
  });
  navigation.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
    button.setAttribute("aria-expanded", "false");
    navigation.classList.remove("is-open");
  }));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navigation.classList.contains("is-open")) {
      button.setAttribute("aria-expanded", "false");
      navigation.classList.remove("is-open");
      button.focus();
    }
  });
});
