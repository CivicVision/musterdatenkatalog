function getWriteInTopic() {
  let el = document.querySelector('#id_write_in-topic')
  return el ? el.value : ''
}
function score() {
  return {
    modeldataset: false,
    modelsubject: false,
    topic: getWriteInTopic(),
    term: '',
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
