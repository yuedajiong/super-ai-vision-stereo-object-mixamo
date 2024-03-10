const syncWait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function fireEvent(eventElement, eventType) {
  if (typeof eventType === 'string' && typeof eventElement[eventType] === 'function') {
    eventElement[eventType]();
  } else {
    const event = eventType === 'string' ? new Event(eventType, {bubbles: true}) : eventType;
    eventElement.dispatchEvent(event);
  }
}

function listAnimation() {
    return document.querySelectorAll(".product-results-holder .product-animation")
}

const nextAnimation = async () => {
  var lastButton = document.querySelectorAll(".pagination.pagination-sm li:last-child a")
  fireEvent(lastButton[0], "click")
  await syncWait(5*1000)
}

const fullAnimation = async (jspy, nameCharacter) => {
    var a = 0
    fullA = listAnimation()
    for (var j = 0; j <= fullA.length; j++) {
      if (j >= fullA.length) {
        await nextAnimation()
        fullA = listAnimation()
        if (fullA.length == 0) {
          jspy.call('DEBUG'+' $$$ '+'animation done', back)
          break
        }
        a = a + 1
        j = 0
        window.scrollTo(0, document.body.scrollHeight);
      }
      fireEvent(fullA[j], "click")
      await syncWait(5*1000)
      var button_down = document.querySelectorAll(".product-preview-holder .editor.row.row-no-gutter > div.editor-sidebar.col-xs-4 button")[0]
      fireEvent(button_down, "click")
      await syncWait(2*1000)
      var button_sure = document.querySelectorAll(".modal-footer .btn-primary")[0]
      fireEvent(button_sure, "click")
      await syncWait(12*1000)

      nameAnimation = fullA[j].children[2].children[0].children[0].innerText
      jspy.call('Animation'+' $$$ '+nameCharacter+' $$$ '+nameAnimation+' $$$ '+(j.toString()+'/'+fullA.length.toString()+'/'+a.toString()), back);
    }
}

function listCharacter() {
    return document.querySelectorAll(".product-results-holder .product-character")
}

const nextCharacter = async () => {
  var lastButton = document.querySelectorAll(".pagination.pagination-sm li:last-child a")
  fireEvent(lastButton[0], "click")
  await syncWait(10*1000)
}

const fullCharacter = async (jspy, role) => {
    tabs = document.querySelectorAll(".nav-tabs")[0].children
    fireEvent(tabs[0].children[0], "click")
    await syncWait(5*1000)

    var c = 0
    fullC = listCharacter()
    for (var i = 0; i <= fullC.length; i++) {
      if (i >= fullC.length) {
        await nextCharacter()
        fullC = listCharacter()
        if (fullC.length == 0) {
          jspy.call('DEBUG'+' $$$ '+'character done', back)
          break 
        }
        c = c + 1
        i = 0
        window.scrollTo(0, document.body.scrollHeight);
      }

	  nameCharacter = fullC[i].children[2].children[0].children[0].innerText
      if (Number.isInteger(role) && role==c*96+i) {
		jspy.call('Character'+' $$$ '+nameCharacter+' $$$ '+(i.toString()+'/'+fullC.length.toString()+'/'+c.toString()), back);

        tabs = document.querySelectorAll(".nav-tabs")[0].children
		fireEvent(tabs[0].children[0], "click")
		await syncWait(5*1000)

		fireEvent(fullC[i], "click")
		await syncWait(5*1000)

		tabs = document.querySelectorAll(".nav-tabs")[0].children
		fireEvent(tabs[1].children[0], "click")
		await syncWait(5*1000)

		fullAnimation(jspy, nameCharacter)
		await syncWait(26*96*30*1000)
      } else {
        jspy.call('DEBUG'+' $$$ '+'character skip: '+nameCharacter+' '+'role='+role.toString()+' c='+c.toString()+' '+'i='+i.toString(), back)
      }  
  }
}

function back(result) {
	console.log('back: '+result)
}
function init(role) {
	var objects;
	new QWebChannel(qt.webChannelTransport, function(channel) {
		jspy = channel.objects.jspy;
        jspy.call('DEBUG'+' $$$ '+'JsPy init', back)
        fullCharacter(jspy, role);
	})
}

