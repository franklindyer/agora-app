'use strict';

/*
Goal: use js to save progress of post and report writing, so that if a user leaves / refreshes the page / has to log in again, the post / report will be waiting for them when they return.
*/

document.addEventListener('DOMContentLoaded', function() {
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
}, false);

/*
Goal: combine all reCaptcha scripts into one function defined here.
*/

/*
Goal: create a text box that can be used for posts, report writing, comments, status box, etc. that will resize itself dynamically as its content grows and shrinks.
*/

/*
Goal: create a "confirmation" field that will be used when a user is entering important information (such as their email or password) that we want to verify is the same information entered both times.
*/

