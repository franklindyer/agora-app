'use strict';

/**
 * These actions will be carried out when the page is finished loading.
 */
document.addEventListener('DOMContentLoaded', function() {
    setUpPostEditing();
    verifyInputMatch();
}, false);

/*
Goal: create a "confirmation" field that will be used when a user is entering important 
      information (such as their email or password) that we want to verify is the same 
      information entered both times.
*/

function verifyInputMatch() {
    const ogField = document.getElementById('password');
    const cnfField = document.getElementById('password-confirm');
    if(ogField && cnfField) {
        cnfField.addEventListener('input', () => {
            const match_notice = document.getElementById('match-notice');
            const submit = document.getElementById('captcha-submit');
            if((cnfField.value == '') || (cnfField.value == ogField.value)) {
                match_notice.style.setProperty('display', 'none');
                submit.disabled = false;
            } else {
                match_notice.style.setProperty('display', 'block');
                submit.disabled = true;
            }
        });
    }
}


/**
 * This function will check if the page has elements to indicate that we are writing or editing 
 * a post, and if so, will set up localStorage to save the progress of the post during editing. 
 * The post area will also be populated with any currently associated localStorage values.
 */
function setUpPostEditing() {
    const titleContainer = document.getElementsByClassName('post-box')[0];
    const bodyContainer = document.getElementsByClassName('post-box')[1];
    if(titleContainer && bodyContainer) { // We are writing or editing a post
        const title = titleContainer.children[0];
        if(!localStorage.getItem(title.id)) {
            /* if there's no existing localStorage entry of this type, then create one and 
               populate it with whatever value exists within the post already */
            localStorage.setItem(title.id, title.value);
        }
        title.addEventListener('input', () => {
            // update the item every time its input is changed
            localStorage.setItem(title.id, title.value);
        });
        title.value = localStorage.getItem(title.id);

        const body = bodyContainer.children[0];
        if(!localStorage.getItem(body.id)) {
            localStorage.setItem(body.id, body.value);
        }
        body.addEventListener('input', () => {
            localStorage.setItem(body.id, body.value);
        });
        body.value = localStorage.getItem(body.id);
    }
    return;
}

/*
Goal: Create timestamps for user-visible actions that are based on a user's time zone.
*/

/*
Goal: combine all reCaptcha scripts into one function defined here.
*/

/*
Goal: create a text box that can be used for posts, report writing, comments, status box, etc. 
      that will resize itself dynamically as its content grows and shrinks.
*/

