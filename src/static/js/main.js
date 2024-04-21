'use strict';

/**
 * These actions will be carried out when the page is finished loading. This setup will likely
 * be changed in the future, but it's working for now on a small scale.
 */
document.addEventListener('DOMContentLoaded', function() {
    setUpPostEditing();
    verifyInputMatch();
    adjustTimeZone();
    updateSettingPasswordCheck();
}, false);

/**
 * This function searches the page for timestamp elements and then updates the timezone in each
 * element to be the user's local time.
 */
function adjustTimeZone() {
    const timestamps = document.getElementsByClassName('timestamp');
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    var length = timestamps.length;
    var i = 0;
    for(i; i < length; i++) {
        /* the date and time value saved on the server (UTC) vs the user's local time zone */
        var dateServer = new Date(timestamps[i].innerHTML + 'Z');
        var dateUser = new Date(dateServer.toLocaleString('en-US', { timeZone: timeZone }));
        
        const formattedDate = dateUser.toLocaleDateString('en-US', {
            weekday: 'long', 
            month: 'long', 
            day: 'numeric', 
            year: 'numeric' 
        });
        const formattedTime = dateUser.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        timestamps[i].innerHTML = formattedDate + ' at ' + formattedTime;
    }
}

/**
 * This function makes a password verification field appear if the user is trying to update 
 * their email. This can be further abstracted in the future.
 */
function updateSettingPasswordCheck() {
    const emailForm = document.getElementById('update-existing-email');
    if(emailForm) {
        const passwordField = document.getElementById('password-field');
        emailForm.addEventListener('input', () => {
            passwordField.style.setProperty('visibility', 'visible');
        });
    }
}

/**
 * This function enables the behavior of the password confirmation field if on the account
 * creation page. This can be further abstracted in the future.
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
    const title = document.getElementsByClassName('post-box')[0];
    const body = document.getElementsByClassName('post-box')[1];
    if(title && body) { // We are writing or editing a post
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
Goal: combine all reCaptcha scripts into one function defined here.
*/

/*
Goal: create a text box that can be used for posts, report writing, comments, status box, etc. 
      that will resize itself dynamically as its content grows and shrinks.
*/

