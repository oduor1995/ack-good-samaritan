/* Project specific Javascript goes here. */
document.addEventListener('DOMContentLoaded', function () {
  var dropdownToggleList = document.querySelectorAll(
    '[data-bs-toggle="dropdown"]',
  );
  dropdownToggleList.forEach(function (dropdownToggle) {
    new bootstrap.Dropdown(dropdownToggle);
  });
});
