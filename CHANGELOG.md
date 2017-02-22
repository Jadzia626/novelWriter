## novelWriter Change Log

#### Version 0.4 - Under development
* **GUI:** Added about dialog.
* **Code:** Book files are now only saved when there is an actual change in data. Previously it would simply just overwrite files, which is not ideal when using file sync software.

#### Version 0.3 - 19.01.2017
* **GUI:** The state of the spell checker and show paragraph buttons are now saved between sessions.
* **GUI:** There is now a dialog window for preferences.
* **GUI:** Added a dialog window under Menu > View > Scene Buffer. This dialog shows all open scenes. Mainly added for debuging purposes, and may later be hidden when the application is not running in debugging mode.
* **Code:** Moved a lot of the checks to make sure data is saved properly into the book subpackage so that the checks and logic all exists in the most natural place in the code.
* **Code:** Made changes to the Book class so that it holds several open scenes in a dictionary of objects. These are kept open for five minutes after the scene is no longer being edited.

#### Version 0.2.1 - 17.01.2017
* Removed Undo/Redo/Cut/Copy/Paste from menu as the key bindings overrides default functionality for widget in focus. These are unnessecary anyway as the WebView editor already have the neede functionality implemented.
* Added Paste Plain Text and Paste Clean HTML as options instead. However these functions have not yet been implemented.
* Minor changes to Open Recent submenu.
* Added button to enable/disable spellchecking. This uses the internal spell checker functionality in the WebView editor. This also sets the language to the default language defined in the config file.
* Web editor context menu was previously disabled to prevent move in history and reload (which would interupt the editor functionality). Now it is enabled in editing mode only, which gives access to spell checking, and clipboards functionality.
* Status bar now contains more information than just a LED light for saved/unsaved text buffers. The yellow LED indicates the text has been autosaved, which means there may be unsaved metadata still.
* Status bar now also shows which file is being edited, which file handle it has (needed if you want to look up the physical file in the data folder), and what language for spell checking the editor is currently set to.

#### Version 0.2 - 15.01.2017
* Completely replaced the data wrapper classes with a book subpackage.
* Menu items are now connected, and Open Recent feature added.
* Designed some new buttons and made some code changes to how they're loaded.
* Numerous bug fixes to data handling, but may still be unstable and data could potentially be overwritten.

#### Version 0.1 - 13.01.2017
* Initial pre-release. No changes.