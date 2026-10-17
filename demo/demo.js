(() => {
  const approve = document.getElementById('approve');
  const deny = document.getElementById('deny');
  const status = document.getElementById('status');
  let decided = false;
  function choose(choice) {
    if (decided) return;
    decided = true;
    approve.disabled = deny.disabled = true;
    status.dataset.choice = choice;
    status.textContent = (choice === 'approve' ? 'Approved for this demo.' : 'Demo request denied.') + ' No command ran.';
  }
  approve.addEventListener('click', () => choose('approve'));
  deny.addEventListener('click', () => choose('deny'));
})();
