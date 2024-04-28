console.log('loaded preload-view.js');

const { ipcRenderer,
        // contextBridge
      } = require('electron');

let action_list = [];

ipcRenderer.on('mark-page', (event, state, payload) => {
  markPage();
});

ipcRenderer.on('navigate-webview', (event, action, payload) => {
  console.log('navigate on prelaod-view called');
    switch (action) {
        case 'back':
            if (window.history.length > 1) {
                window.history.back();
            }
            break;
        case 'forward':
            if (window.history.length > 1) {
                window.history.forward();
            }
            break;
        case 'reload':
            window.location.reload();
            break;
        case 'loadURL':
            window.location.href = payload;
            break;
    }
});

async function handleMouseInteraction(event) {
  // Log the event type and the target element
  console.log('Mouse interaction detected:', event.type, '\nTarget element:', event.target);
  const payload = {
    "type": event.type,
    "coordinate": [event.clientX, event.clientY],
    "element": {
      "tag": event.target.tagName,
      "text": event.target.innerText
    }
  };
  action_list.push(payload);

  // back to electron
  ipcRenderer.send('webview:click-action', payload);
}

function get_actions(){
  let jlist = JSON.stringify(action_list);
  action_list = []; // clean actions?
  return jlist;
}

async function handleScrollInteraction(event){
  console.log('Scroll interaction detected: ', window.scrollY);

  const payload = {
    type: "scroll",
    scrollY: window.scrollY,
  };

  action_list.push(payload);

  // back to electron
  ipcRenderer.send('webview:scroll-action', payload);
}

window.addEventListener('DOMContentLoaded', () => {
  console.log('DOMContentLoaded for preload-view.js');

  document.addEventListener('click', handleMouseInteraction);
  document.addEventListener('dblclick', handleMouseInteraction);
  document.addEventListener("scrollend", handleScrollInteraction);

  ipcRenderer.send('webview:ready');
});


// DOM Labeler
let labels = [];

function unmarkPage() {
  console.log('unmarking page...');
  for(const label of labels) {
    document.body.removeChild(label);
  }

  labels = [];
}

// TODO use vimium's algorithm
function markPage() {
  console.log('markpage called');
  unmarkPage();

  var bodyRect = document.body.getBoundingClientRect();

  var items = Array.prototype.slice.call(
    document.querySelectorAll('*')
  ).map(function(element) {
    var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

    var rects = [...element.getClientRects()].filter(bb => {
      var center_x = bb.left + bb.width / 2;
      var center_y = bb.top + bb.height / 2;
      var elAtCenter = document.elementFromPoint(center_x, center_y);

      return elAtCenter === element || element.contains(elAtCenter);
    }).map(bb => {
      const rect = {
        left: Math.max(0, bb.left),
        top: Math.max(0, bb.top),
        right: Math.min(vw, bb.right),
        bottom: Math.min(vh, bb.bottom)
      };
      return {
        ...rect,
        width: rect.right - rect.left,
        height: rect.bottom - rect.top
      };
    });

    var area = rects.reduce((acc, rect) => acc + rect.width * rect.height, 0);

    return {
      element: element,
      include:
        (element.tagName === "INPUT" || element.tagName === "TEXTAREA" || element.tagName === "SELECT") ||
        (element.tagName === "BUTTON" || element.tagName === "A" || (element.onclick != null) || window.getComputedStyle(element).cursor == "pointer") ||
        (element.tagName === "IFRAME" || element.tagName === "VIDEO")
      ,
      area,
      rects,
      text: element.textContent.trim().replace(/\s{2,}/g, ' ')
    };
  }).filter(item =>
    item.include && (item.area >= 20)
  );

  // Only keep inner clickable items
  items = items.filter(x => !items.some(y => x.element.contains(y.element) && !(x == y)));

  // Function to generate random colors
  function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  // Lets create a floating border on top of these elements that will always be visible
  items.forEach(function(item, index) {
    item.rects.forEach((bbox) => {
      newElement = document.createElement("div");
      var borderColor = getRandomColor();
      newElement.style.outline = `2px dashed ${borderColor}`;
      newElement.style.position = "fixed";
      newElement.style.left = bbox.left + "px";
      newElement.style.top = bbox.top + "px";
      newElement.style.width = bbox.width + "px";
      newElement.style.height = bbox.height + "px";
      newElement.style.pointerEvents = "none";
      newElement.style.boxSizing = "border-box";
      newElement.style.zIndex = 2147483647;
      // newElement.style.background = `${borderColor}80`;

      // Add floating label at the corner
      var label = document.createElement("span");
      label.textContent = index;
      label.style.position = "absolute";
      label.style.top = "-19px";
      label.style.left = "0px";
      label.style.background = borderColor;
      label.style.color = "white";
      label.style.padding = "2px 4px";
      label.style.fontSize = "12px";
      label.style.borderRadius = "2px";
      newElement.appendChild(label);

      document.body.appendChild(newElement);
      labels.push(newElement);
      // item.element.setAttribute("-ai-label", label.textContent);
    });
  });

  ipcRenderer
    .send('label-data',
          JSON.stringify(
            items
              .map(item => ({
                x: (item.rects[0].left + item.rects[0].right) / 2,
                y: (item.rects[0].top + item.rects[0].bottom) / 2,
                bboxs: item.rects.map(({left, top, width, height}) => [left, top, width, height])
              }))));

}

// NOTE In case we need to send and receive data back from electron
// contextBridge.exposeInMainWorld('danger-api', {
//   ping: () => ipcRenderer.invoke('debug:ping'),
// });

// contextBridge.exposeInMainWorld('electronAPI', {
//   onUpdateCounter: (callback) => ipcRenderer.on('update-counter', (_event, value) => callback(value)),
//   counterValue: (value) => ipcRenderer.send('counter-value', value)
// })


