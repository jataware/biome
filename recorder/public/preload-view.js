
// const customCSS = `
//     ::-webkit-scrollbar {
//         width: 10px;
//     }

//     ::-webkit-scrollbar-track {
//         background: #27272a;
//     }

//     ::-webkit-scrollbar-thumb {
//         background: #888;
//         border-radius: 0.375rem;
//     }

//     ::-webkit-scrollbar-thumb:hover {
//         background: #555;
//     }
// `;


console.log('preload-view from gpt4-act within scooter recorder');

window.addEventListener('DOMContentLoaded', () => {
  alert('hello from webview...');
    // const styleTag = document.createElement('style');
    // styleTag.textContent = customCSS;
    // document.head.append(styleTag);
});




// const { ipcRenderer } = require('electron'); // ?


// Listen for messages from preload.js to navigate
// ipcRenderer.on('navigate-webview', (event, action, payload) => {
//     switch (action) {
//         case 'goBack':
//             if (window.history.length > 1) {
//                 window.history.back();
//             }
//             break;
//         case 'goForward':
//             if (window.history.length > 1) {
//                 window.history.forward();
//             }
//             break;
//         case 'reload':
//             window.location.reload();
//             break;
//         case 'loadURL':
//             window.location.href = payload;
//             break;
//     }
// });


// Send the current URL whenever it changes
// window.addEventListener('load', () => {
//     ipcRenderer.send('current-url', window.location.href);

//     let oldHref = document.location.href;
//     const body = document.querySelector("body");
//     const observer = new MutationObserver(mutations => {
//         if (oldHref !== document.location.href) {
//             oldHref = document.location.href;
//             ipcRenderer.send('current-url', window.location.href);
//         }
//     });
//     observer.observe(body, { childList: true, subtree: true });
// });

// window.addEventListener('beforeunload', () => {
//     ipcRenderer.send('current-url', window.location.href);
// });

// window.addEventListener('popstate', () => {
//     ipcRenderer.send('current-url', window.location.href);
// });


// ipcRenderer.on('observer', (event, state, payload) => {
//   switch (state) {
//       case 'screenshot-start':
//           markPage();
//           break;
//       case 'screenshot-end':
//           unmarkPage();
//           break;
//   }
// });

// DOM Labeler
let labels = [];

function unmarkPage() {
  console.log('unmark page called');
  for(const label of labels) {
    document.body.removeChild(label);
  }

  labels = [];
}

function markPage() {
  console.log('mark page called');

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

      return elAtCenter === element || element.contains(elAtCenter) 
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
  items = items.filter(x => !items.some(y => x.element.contains(y.element) && !(x == y)))

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
      let newElement = document.createElement("div");
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
  })

  console.log('label data', items);

  // ipcRenderer.send('label-data', JSON.stringify(items.map(item => {
  //   return {
  //       x: (item.rects[0].left + item.rects[0].right) / 2, 
  //       y: (item.rects[0].top + item.rects[0].bottom) / 2,
  //       bboxs: item.rects.map(({left, top, width, height}) => [left, top, width, height])
  //   }
  // })));

}
