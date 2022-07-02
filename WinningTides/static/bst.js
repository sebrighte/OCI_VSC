function isBST(date) {
  function lastSunday(month, year) {
    var d = new Date();
    var lastDayOfMonth = new Date(Date.UTC(year || d.getFullYear(), month + 1, 0));
    var day = lastDayOfMonth.getDay();
    return new Date(Date.UTC(lastDayOfMonth.getFullYear(), lastDayOfMonth.getMonth(), lastDayOfMonth.getDate() - day));
  }
  var d = date || new Date();
  var starts = lastSunday(2, d.getFullYear());
  starts.setHours(1);
  var ends = lastSunday(9, d.getFullYear());
  starts.setHours(1);
  return d.getTime() >= starts.getTime() && d.getTime() < ends.getTime();
}

function UTC2BST(date) {
  var d = date || new Date();
  if (isBST(d)) {
    d.setHours(d.getHours() + 1);
    return d;
  }
  return d;
}