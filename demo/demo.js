(() => {
  const approve = document.getElementById('approve');
  const deny = document.getElementById('deny');
  const status = document.getElementById('status');
  let decided = false;
  function choose(choice) {
    if (decided) return;
    decided = true;
    approve.disabled = deny.disabled = true;
    status.textContent = choice + ' tapped. No command ran.';
  }
  approve.addEventListener('click', () => choose('Approve demo'));
  deny.addEventListener('click', () => choose('Deny demo'));
})();
