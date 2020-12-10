function score() {
  return {
    modeldataset: false,
    modelsubject: false,
    popup: false,
    setModelsubject(id) {
      let el = document.querySelector('input.modelsubject[value="'+id+'"]')
      el.checked = true;
    },
    setModeldataset(id) {
      let el = document.querySelector('input.modeldataset[value="'+id+'"]')
      el.checked = true;
    },
  };
}
