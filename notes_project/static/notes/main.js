$(function() {
  initFooterDate();
});

function initFooterDate() {
    let d = new Date();
    let strDate = d.getFullYear();
    $('#footer-date').text(strDate)
}