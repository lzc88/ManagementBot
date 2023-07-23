

<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")



            **<span style="text-decoration:underline;">Orbital 2023 Milestone 3 Report</span>**

**Team Name: Deadline Defenders (5568)**

**Team Members: Lim Zhi Chao & Ang Qi Wei Chester**

**Proposed Level of Achievement: Apollo 11**

**Project Name : ManagementBot**

**<span style="text-decoration:underline;">Motivation</span>**

University students **often have too much on their plate**. Catching up on lecture videos, meeting assignment deadlines, attending group projects… These are only a few of the many struggles a university student encounters. **It can be confusing and stressful to manage** **when assignments pile up**. The added stress from disorganization can cause one to be disoriented, hence **compromising productivity**. By utilizing Telegram, a popular messaging app with a user-friendly interface, a student’s schedule and deadlines can be **better organized**.  With a **clearer picture** on what needs to be done, and when it will be due, students can **better manage their time and avoid unintended stress**, thus improving their mental health. Having an easily accessible planner would definitely appeal to the needs of most students.

**<span style="text-decoration:underline;">Aim</span>**

We hope that our telegram bot will be able to help university students manage their assignments. By providing reminders, tracking assignments, and offering resources, the bot can help to reduce stress and improve productivity. Our main goal is to create a user-friendly bot that students can easily access and utilize to better manage their coursework and achieve their academic goals.

**<span style="text-decoration:underline;">User Stories</span>**



1. I am a **university student** who wants to have an automated **consolidated list of my assignment deadlines** so that I will not **accidentally miss out on any important deadlines**.
2. I am a **university student** who wants to have an **accessible, updated weekly timetable and personal planner** so that I can have an **easier time making personal or school related plans**.
3. I am a **university student** who wants to have a **clear picture of upcoming lectures and assignments** so that I can **better focus on my revision** without being stressed.
4. I am **an NUS student who uses the NUSMods platform**. I want to have an accessible platform to **access my modules and timetables conveniently** so that I don’t have to constantly change platforms for reference. (Also not having to re-enter my modules and timetables whenever I clear my browser history and cache)

**<span style="text-decoration:underline;">Features</span>**

**Bot Name: ManagementBot @dlmanage_bot on Telegram**

For our project, we would make use of Telegram, a messaging app which many students are using, hence making our bot very accessible to most of these students.

The **Telegram Bot **provides a chat-like interface for users to easily access desired information.

Tech Stack:



1. Python with pyTelegramBotAPI package
2. Firebase as database
3. Replit for hosting

You can access our GitHub repository at [https://github.com/lzc88/managementbot](https://github.com/lzc88/managementbot)

Note: Although you may see the backend code in the repo, **PLEASE DO NOT RUN THE PYTHON SCRIPT.** ** Please import in your own bot token and firebase credentials** if you wish to run our code in the GitHub.

**<span style="text-decoration:underline;">ManagementBot Functions</span>**

In the Main Menu, the user will be offered keyboard pop ups to prompt their next course of action. There are 6 functions the user can choose from. For each function, there will be a **“Return to Main”** option which will direct them back to the **Main Menu**.

**The ManagementBot has 6 main functions in the Main Menu:**



1. **Assignment Deadlines**
2. **Personal Planner**
3. **School Timetable**
4. **Exam Timetable**
5. **View Modules**
6. **Report Issues**

**Additional functions:**



1. **Reminders**
2. **Auto deletion of past dl/event**

**{1} [ Initializing the bot with /start command and Main Menu ]**


```

```


To initialize the bot ( for first time users ), the user can simply tap on the **Start** pop up (Figure 1.1)

If the user is a new user, the bot will prompt the user to **key in the module code** by asking what modules he/she is taking this semester. (Figure 1.2) After keying in the first module code, the user can choose what to do next. (Figure 1.3)

Else, the bot will greet the user and display the **Main Menu **(Figure 1.4) with options that they can proceed with.


<table>
  <tr>
   <td>

<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image2.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 1.1</strong>
   </td>
   <td>

<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image3.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 1.2</strong>
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image4.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image4.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 1.3</strong>
   </td>
   <td>

<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image5.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image5.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 1.4</strong>
   </td>
  </tr>
</table>


**{2} [ Function 1 : Assignment Deadlines ]**


```

```


This function tracks and displays assignment deadlines of the user. This function can be called by tapping on the **Assignment Deadlines** option in the **Main Menu**.

By default, the assignment deadlines list is empty. Hence the user will be prompt to add deadlines.


<table>
  <tr>
   <td>

<p id="gdcalert6" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image6.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert7">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image6.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>“<strong>Assignment Deadlines</strong>” list out all deadlines in the following format as such
<p>
index) Title:
<p>
           Due_date:
<p>
           Time_left:
<p>
           Status: 
<p>
while sorting the time left in chronological order such that the approaching deadline will be at the top of the list. Assignments that are marked INCOMPLETE will also be prioritized at the top over COMPLETED assignments.
<p>
If the user does not have any deadlines, the bot will inform the user that they do not have any pending deadlines.
<p>
In addition, any assignment past >24 hours the due date will be automatically deleted from the user’s database.
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert7" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image7.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert8">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image7.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>One sub function is “<strong>Mark Assignments as complete</strong>” which allows the user to mark assignments whose status are “INCOMPLETE” to “COMPLETED”. The user will be presented with a list of all the deadlines that can be marked “COMPLETED” in which they may choose the assignment name on the buttons. After which the bot will process their request and update the status of the chosen deadline.
<p>
The Assignment Deadline list will be automatically called back, and the COMPLETED assignment will be pushed to the bottom of the list so that priority is given to approaching “INCOMPLETE” deadlines.
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert8" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image8.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert9">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image8.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>Another sub function is “<strong>Mark Assignments as incomplete</strong>”, which allows the user to mark assignments whose status are “ COMPLETED” to “INCOMPLETE”. This works similar to the previous “<strong>Mark Assignments as complete</strong>” sub function.
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert9" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image9.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert10">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image9.png" width="" alt="alt_text" title="image_tooltip">


<p id="gdcalert10" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image10.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert11">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image10.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>Another sub function “<strong>Manage Deadlines Data</strong>”, which allows users to both add and delete deadlines.
<p>
 “<strong>Add Deadline</strong>” is a 2-step process
<ol>

<li>The user will shall enter the deadline name

<li>The user will set the time of this deadline, in the format of DD/MM HHMM (the current year will be automatically added in). Subsequently, the user may type in the full format DD/MM/YYYY HHMM

<p>
Valid deadlines will be stored into the user’s database (dl_data) which will then be displayed on the main assignment deadlines list.
<p>
The user may also choose to “<strong>Delete Deadline</strong>”, in which all valid events will be shown on buttons, in which the user may choose to delete. (Note that only events that are manually added from “Add Deadline” can be deleted, as it is independent from deadlines retrieved from canvas calendar). Upon selection, the selected deadline will be deleted from the user’s database.
<p>
Subsequently, the user may manually type in “<strong>DELETE_ALL_DEADLINES</strong>” to delete all deadlines (including canvas calendar deadlies)
</li>
</ol>
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert11" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image11.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert12">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image11.png" width="" alt="alt_text" title="image_tooltip">

<p>


<p id="gdcalert12" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image12.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert13">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image12.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>“<strong>Manage Calendar Data</strong>” serves to allow users to link their own canvas calendar link (which is personal to one canvas account and doesn’t change) into the user’s database. Upon calling the function “<strong>Provide Canvas Calendar .ics link</strong>” , the bot will prompt the user to send their own canvas calendar link. Upon sending the link, the bot will then store this link into the user’s database. 
<p>
(Note that if your canvas does not have any valid deadlines e.g No deadlines that are past due, then it will not be shown. Since it is currently holiday break, to test this, please manually add your own valid assignments on canvas to test. Please refer to the next textbox <strong>How does the automatic Canvas Calendar .ics link work? </strong> for more details)
<p>
If an existing .ics link is detected, then the bot will ask if the user wishes to “<strong>Update Calendar .ics link</strong>” or “<strong>Delete Canvas Calendar .ics link</strong>”. If the user wants to <strong>update</strong>, then the user may send the bot a new .ics link which is then stored over the old .ics link. If the user chooses to <strong>delete </strong>the .ics link, then the link along with all the deadlines associated with the .ics link will be deleted from the user’s database.
   </td>
  </tr>
</table>



<table>
  <tr>
   <td rowspan="4" ><strong><span style="text-decoration:underline;">How does the automatic Canvas Calendar .ics link work?</span></strong>
<ul>

<li>Upon storing the user's .ics link, when the main assignment deadlines function is called, a passive function <strong>retrieve_and_update_ics_data</strong>() is being called which then retrieves all assignments data from the provided link and then stored it in the database, which is subsequently displayed in the deadline list (if any).

<li>In this example, I have stored in my .ics link with no valid assignments on canvas, hence the bot will show that I do not have any assignments.
<p>

    

<p id="gdcalert13" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image13.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert14">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image13.png" width="" alt="alt_text" title="image_tooltip">

<ul>

<li>Now I will head to Canvas Calendar and manually add in a deadline by clicking on the + box, in this case Orbital Milestone 2. This simulates during the semester where module coordinators will add in the assignments to the module canvas page, which will reflect in this canvas calendar.

<p>


<p id="gdcalert14" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image14.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert15">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image14.png" width="" alt="alt_text" title="image_tooltip">


<p id="gdcalert15" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image15.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert16">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image15.png" width="" alt="alt_text" title="image_tooltip">

<ul>

<li>Now I will call the main Assignment Deadlines function again, which passively calls <strong>retrieve_and_update_ics_data</strong>() to check the .ics data, and it will detect the newly added Orbital Milestone 2 and subsequently update it into the user’s database. Events that are also deleted from the canvas calendar will also be updated on the bot upon calling the Assignment Deadlines function.
<p>

    

<p id="gdcalert16" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image16.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert17">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image16.png" width="" alt="alt_text" title="image_tooltip">

</li>
</ul>
</li>
</ul>
</li>
</ul>
   </td>
  </tr>
  <tr>
  </tr>
  <tr>
  </tr>
  <tr>
  </tr>
  <tr>
   <td><strong><span style="text-decoration:underline;">How does the bot send reminders of approaching deadlines?</span></strong>
<ul>

<li>Upon initializing the bot by calling<strong> /start</strong>, a recursive function <strong>check_deadline_reminders()</strong> calls itself every minute to check the time left on all valid deadlines which status are marked as “INCOMPLETE” <strong>(Deadlines marked as “COMPLETED” will not receive any reminders)</strong> and then send the appropriate reminder. Currently the bot will send a reminder if the deadline is  [ 72 hours , 24 hours , 6 hours , 1 hour , is due ] from the due date. Each countdown interval will only be sent once to avoid spamming.
<p>

    

<p id="gdcalert17" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image17.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert18">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image17.png" width="" alt="alt_text" title="image_tooltip">

<ul>

<li>With the example deadline Due test above, when I loaded the list at 1317 hrs, there was still a minute left before it was officially due. Once it is due at 1318 hrs, then the bot sends me a message to inform me that it is due.
<p>

    

<p id="gdcalert18" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image18.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert19">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image18.png" width="" alt="alt_text" title="image_tooltip">

<ul>

<li>Here is another example, except that it is an hour before the due date.

<p>
Note that you do not need to be online / on assignments deadline list page for this to work, as long as this separate recursive function is running in the background doing the checks.
</li>
</ul>
</li>
</ul>
</li>
</ul>
   </td>
  </tr>
  <tr>
   <td><strong><span style="text-decoration:underline;">In the event of more than >8 valid deadlines in the list.</span></strong>
<ul>

<li>Due to character limits in which a bot can send, in the event that there are >8 valid deadlines, the bot will split the list to multiple pages (max 8 per page) which can be navigated using “<strong>Next page</strong>” and “<strong>Previous page</strong>” buttons which only appear under this circumstance.

<li>From the 3 images below, we can see that the button ‘Next page’ is present with the additional text “Please click on the ‘Next’ button to view more deadlines”. Upon clicking on “<strong>Next page</strong>”, the bot will process the 2nd page of the assignments deadline list and then display them. We can see that since there are only 2 pages, the 2nd page will only have the “<strong>Previous page</strong>” button, which upon selecting will then generate the 1st page of the assignments deadline list. There can be more than 2 pages.
<p>

    

<p id="gdcalert19" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image19.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert20">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image19.png" width="" alt="alt_text" title="image_tooltip">


<p id="gdcalert20" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image20.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert21">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image20.png" width="" alt="alt_text" title="image_tooltip">


<p id="gdcalert21" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image21.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert22">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image21.png" width="" alt="alt_text" title="image_tooltip">

</li>[Uploading 5568 Milestone 3 README.zip…]()

</ul>
   </td>
  </tr>
</table>



```
How user's canvas calendar data is being stored on the firestore



Under collection cc_data, the ics_link is stored under document ics_link, which is used to auto update the assignments document with the data in the canvas calendar link. The deadlines is being stored under document assignments with the field as deadline name which contains the due_date and the status (indicate COMPLETED or INCOMPLETE)

How user's manual deadline is being stored on the firestore


Under collection dl_data, assignments document, the deadlines is being stored with the field as deadline name which contains the due_date and the status (indicate COMPLETED or INCOMPLETE)
```


**{3} [Function 2: Personal Planner]**


```

```



<table>
  <tr>
   <td>

<p id="gdcalert22" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image22.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert23">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image22.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>“<strong>Personal Planner</strong>” fetches the user’s own Personal Planner (if any) in the format as such. 
<p>
Index) Event Name
<p>

    Date
<p>

    Time to event
<p>

    Additional Notes (*Optional)
<p>
This will allow the user to create their own personal planner and will be entirely up to the user on how they wish to use it, similar to how a calendar app will work.
<p>
Any event past >24 hours from the event time will be automatically deleted from the user’s database.
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert23" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image23.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert24">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image23.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>One sub function is “<strong>Add Events</strong>” which is a 3-step process. 
<ol>

<li>The user will shall enter the event name

<li>The user will set the time of this event, in the format of DD/MM HHMM (the current year will be automatically added in). Subsequently, the user may type in the full format DD/MM/YYYY HHMM

<li>The bot will ask the user whether they want to add in additional comment, if yes, then the user may type in their desired note and the bot will process it and add the event. If not, the bot will automatically mark the notes as an empty string and add in the event
</li>
</ol>
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert24" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image24.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert25">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image24.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>One sub function is “<strong>Delete Events</strong>”, in which the user can delete an added event by selecting the corresponding index. 
<p>
Subsequently if the user wishes to delete all events, they may type in “<strong>Delete_all_personal_planner</strong>” to do so.
   </td>
  </tr>
  <tr>
   <td colspan="2" ><strong><span style="text-decoration:underline;">How does the bot send reminders of approaching events?</span></strong>
<ul>

<li>Upon initializing the bot by calling<strong> /start</strong>, a recursive function <strong>check_events_reminders()</strong> calls itself every minute to check the time left on all valid deadlines and then send the appropriate reminder. Currently the bot will send a reminder if the event is  [ 24 hours , 1 hour , 5 mins , now ] from the event time. Each countdown interval will only be sent once to avoid spamming.

<p>


<p id="gdcalert25" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image25.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert26">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image25.png" width="" alt="alt_text" title="image_tooltip">

<p>
Note that you do not need to be online / on a personal planner list page for this to work, as long as this separate recursive function is running in the background doing the checks.
</li>
</ul>
   </td>
  </tr>
</table>



```
How user's personal planner data is being stored on the firestore


Each document under collection personal planner is a unique ID for each event created, which contains date, the additional note, and event name.
```


**{4} [ Function 3 : School Timetable ]**

This function generates and **displays the upcoming schedule of lectures and tutorials** the user has for that particular week. The upcoming lessons are displayed in chronological order. This function can be called by tapping on the **School Timetable** option in the **Main Menu**.

Before generating the timetable, the bot will check if the user has any **unconfigured** **lessons **( user has yet to indicate the lesson slots ).

If there are unconfigured lessons, the user will be shown a **list of unconfigured lessons** and are given the following options to proceed: (Figure 4.1)



1. **Configure lessons**
2. **Unconfigure lessons**
3. **Ignore and proceed to view school timetable**
4. **Return to Main**

Else, the bot will proceed to fetch the user’s upcoming lessons. (Figure 4.8)

If the user **has no modules added**, they will be prompted to add modules.



1. **Configure lessons ( Function 3 )**

The User will be shown keyboard options for them to **decide which lesson to configure**. (Figure 4.2)

The bot will then prompt the user to input the **lesson slot number** for the selected lesson. (Figure 4.3)

 \
If the lesson slot number is valid, the bot will inform the user of successful configuration and check again any remaining unconfigured lessons. (Figure 4.4)

Else, the bot will inform the user that the slot number cannot be found and the lesson will remain unconfigured.


<table>
  <tr>
   <td>

<p id="gdcalert26" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image26.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert27">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image26.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 4.1</strong>
   </td>
   <td>

<p id="gdcalert27" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image27.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert28">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image27.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 4.2</strong>
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert28" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image28.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert29">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image28.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 4.3</strong>
   </td>
   <td>

<p id="gdcalert29" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image29.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert30">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image29.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 4.4</strong>
   </td>
  </tr>
</table>




2. **Unconfigure lessons ( Function 3 )**

The User will be shown keyboard options for them to **decide which lesson (configured) to unconfigure** (Figure 4.5).

The bot will then inform the user that the lesson has successfully been unconfigured, and it will check for unconfigured lessons again. (Figure 4.6)

If there are no configured lessons, the bot will inform the user and check for unconfigured lessons again. (Figure 4.7 )


<table>
  <tr>
   <td>

<p id="gdcalert30" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image30.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert31">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image30.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 4.5</strong>
   </td>
   <td>

<p id="gdcalert31" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image31.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert32">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image31.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 4.6</strong>
   </td>
  </tr>
  <tr>
   <td colspan="2" >

<p id="gdcalert32" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image32.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert33">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image32.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 4.7</strong>
   </td>
  </tr>
</table>




3. **Ignore and proceed to view school timetable ( Function 3 )**

The bot displays the timetable for **configured lessons only**. The timetable is displayed in chronological order and completed lessons are not displayed. (Figure 4.8)

If the user **does not have any configured lessons**, or if the user has **no more upcoming lessons** for the week, the bot will inform the user that he/she has no more lessons for the week and return the user back to the **Main Menu**. (Figure 4.9)


<table>
  <tr>
   <td>

<p id="gdcalert33" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image33.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert34">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image33.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 4.8</strong>
   </td>
   <td>

<p id="gdcalert34" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image34.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert35">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image34.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 4.9</strong>
   </td>
  </tr>
</table>


**{5} [ Function 4 : Exam Timetable ]**


```

```


This function **displays the upcoming examinations to the user. **This function can be called by tapping on the **Exam Timetable** option in the **Main Menu**. (Figure 5.1)

If the user **has no modules added**, they will be prompted to add modules.

The bot will list your finals in** chronological order**, with the day, date, time, duration and countdown being shown. In the event if there is a **clash** in finals, the bot will **send a warning (see bottom message in Figure 5.1)** to inform the user about the clash.

_(Take note that midterm examinations are not shown as information is taken from NUSMods, which only contain data on Final examinations) [ Users may opt to add their Midterm as an assignment using ‘Manage Deadline Data’ -> ‘Add Deadline’ ]_


```

Figure 5.1
```



```
How is exam timing stored in database

Under adding modules, the collection exams will be updated by extracting out exam timing with NUSMODS API and store the datetime of said exam and the duration. The module code is being stored as a field, [0] which is exam date time and [1] is the duration in minutes.
```


**{6} [ Function 5 : View Modules ]**


```

```


This function **displays the list of modules the user has added to their list**. They will then be given the following options to decide on how to proceed: (Figure 6.1) This function can be called by tapping on the **View Modules** option in **Main Menu**.



1. **Add module**
2. **Delete module**
3. **Return to Main**

If the user has **no modules to view**, the bot will inform the user and prompt him/her to add modules.



1. **Add module ( Function 5 )**

The bot will prompt the user to key in the **module code** of the module which he/she would like to add. (Figure 6.2)

If the **module code is valid**, the bot will inform the user that it has successfully added the module and return to the View Modules page. (Figure 6.3)  If the module has **already been added before**, the user will be informed and they will be asked on how to proceed. (Figure 6.5)

**Else**, if invalid,  the bot will inform the user and prompt his/her next decision. (Figure 6.4)


<table>
  <tr>
   <td>

<p id="gdcalert35" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image35.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert36">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image35.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 6.1</strong>
   </td>
   <td>

<p id="gdcalert36" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image36.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert37">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image36.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 6.2</strong>
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert37" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image37.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert38">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image37.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 6.3</strong>
   </td>
   <td>

<p id="gdcalert38" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image38.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert39">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image38.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 6.4</strong>
   </td>
  </tr>
  <tr>
   <td colspan="2" >

<p id="gdcalert39" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image39.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert40">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image39.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 6.5</strong>
   </td>
  </tr>
</table>




2. **Delete module ( Function 5 )**

The bot will prompt the user to select which module he/she would like to delete from the list. (Figure 6.6)

After selecting, the user will be informed of successful deletion and asked on how to proceed. (Figure 6.7)

If the user **has no modules added**, they will be prompted to add modules.


<table>
  <tr>
   <td>

<p id="gdcalert40" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image40.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert41">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image40.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 6.6</strong>
   </td>
   <td>

<p id="gdcalert41" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image41.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert42">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image41.png" width="" alt="alt_text" title="image_tooltip">

<p>
<strong>Figure 6.7</strong>
   </td>
  </tr>
</table>



```
How is mods stored in the database


Under collection mods, modules which you added are then stored as their own document. Under each document, there is a collection 'lessons' which contains details (lecture,lab,tut etc.)



For EC2101, it contains a lecture and tutorial for the module planned instructional methods. For the following classes, config is set to false and will only contain details of the class once configured, which is then used to generate a personal timetable for the user.
```


**{7} [Function 6 : Report Issues]**


```

```



<table>
  <tr>
   <td>

<p id="gdcalert42" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image42.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert43">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image42.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>“<strong>Report Issues</strong>” allows users to submit a bug report or to provide any feedback for the bot. Both have a similar submission structure
<ol>

<li>Input details the feedback/bug 

<li>Bot will ask the user to confirm, which mean user can review their report before submitting, and the user may edit if they wish to do so

<li>Bot will submit their detail to the database where the admin can view them, explained in the next textbox

<p>
Afterwards a successful message appears, indicating that the report is successfully submitted!
</li>
</ol>
   </td>
  </tr>
  <tr>
   <td>

<p id="gdcalert43" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image43.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert44">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image43.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>For admin viewing of the reports, only <strong>approved user_ids</strong> can call the command which will auto generate the full list of bug reports and feedback received.
<p>
Here we can view Status which is either “RESOLVED” or “NOT RESOLVED” and can be edited with 2 sub functions “<strong>Mark Issues as RESOLVED</strong>” and “<strong>Mark Issues as NOT RESOLVED</strong>”. In addition, there is also a sub function “<strong>Edit Issue Notes</strong>” which allows the admin to add in notes onto the reported issues to make reviewing more organized.
<p>
<strong><span style="text-decoration:underline;">This function is not accessible to users.</span></strong>
   </td>
  </tr>
</table>


**<span style="text-decoration:underline;">Diagrams</span>**

**<span style="text-decoration:underline;">User Flow diagrams</span>**

**Link to User Flow diagrams:**

[https://drive.google.com/drive/folders/1uxL6cG_2mB9GtOSHSOUCjWaF1A0Oe3UD?usp=sharing](https://drive.google.com/drive/folders/1uxL6cG_2mB9GtOSHSOUCjWaF1A0Oe3UD?usp=sharing)

**<span style="text-decoration:underline;">Database Schema</span>**



<p id="gdcalert44" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image44.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert45">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image44.png "image_tooltip")


**NOTE:**



1. Structure of **this week’s timetable**:

**{ week_no : [ { lesson_1_data }, { lesson_2_data }, … ]**



2. Structure of **Lesson Weeks**:

**[ List of integers in which the lesson falls on ]**



3. **Current Page** is 1 by default. If User has assignments that exceed one page size ( 8 entries ), **Current Page** will be changed accordingly when User chooses to view the next/previous page of assignments.

**<span style="text-decoration:underline;">Unit Testing</span>**

**/start and Main Menu**


<table>
  <tr>
   <td><strong>Feature</strong>
   </td>
   <td><strong>Expected</strong>
   </td>
   <td><strong>Actual</strong>
   </td>
   <td><strong>Outcome</strong>
   </td>
  </tr>
  <tr>
   <td>New User types ‘start’
   </td>
   <td>Bot greets User
   </td>
   <td>See <strong>Figure 1.2</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Existing User types ‘start’
   </td>
   <td>Bot sends User to Main Menu
   </td>
   <td>See <strong>Figure 1.4</strong>
   </td>
   <td>
   </td>
  </tr>
</table>


**Function 1: Assignment Deadlines**


<table>
  <tr>
   <td><strong>Feature</strong>
   </td>
   <td><strong>Expected</strong>
   </td>
   <td><strong>Actual</strong>
   </td>
   <td><strong>Outcome</strong>
   </td>
  </tr>
  <tr>
   <td>Bot able to determine empty deadline list
   </td>
   <td>Bot informs the user that their deadline list is empty.
   </td>
   <td>

<p id="gdcalert45" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image45.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert46">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image45.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Bot able to list all valid deadlines in correct format and chronological order
   </td>
   <td>Deadlines closer to due_date should be at the top and each dl is displayed in the format
<p>
index) title:
<p>
Due date:
<p>
Time left:
<p>
Status:
   </td>
   <td>

<p id="gdcalert46" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image46.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert47">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image46.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Marking of assignments as completed
   </td>
   <td>The bot accurately lists out all INCOMPLETE deadlines for selection, and then accurately changes selected deadline’s status to “COMPLETED” and is pushed to the bottom of the list.
   </td>
   <td>

<p id="gdcalert47" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image47.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert48">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image47.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Marking of assignments as incomplete
   </td>
   <td>The bot accurately lists out all COMPLETE deadlines for selection, and then accurately changes selected deadline’s status to “INCOMPLETE” and is sorted according to its due_date.
   </td>
   <td>

<p id="gdcalert48" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image48.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert49">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image48.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Add deadline
   </td>
   <td>Bot is able to take the user input deadline title and accept a valid time format, and successfully add it into the database
   </td>
   <td>

<p id="gdcalert49" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image49.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert50">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image49.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Add time for deadline
   </td>
   <td>The bot should recognise Invalid time format and prompt the user to key in a valid time format. If a valid time format is given, then add the deadline into the database.
   </td>
   <td>

<p id="gdcalert50" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image50.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert51">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image50.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Delete deadline
   </td>
   <td>Bot lists out all valid deadlines and accurately deletes the selected deadlines from the user’s database.
   </td>
   <td>

<p id="gdcalert51" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image51.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert52">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image51.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Linking canvas .ics link
   </td>
   <td>Bot is able to prompt and successfully store the .ics link into the database
   </td>
   <td>

<p id="gdcalert52" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image52.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert53">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image52.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Updating canvas .ics link
   </td>
   <td>Bot is able to successfully update the existing .ics link with the new .ics link provided
   </td>
   <td>

<p id="gdcalert53" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image53.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert54">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image53.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Deleting canvas .ics link
   </td>
   <td>Bot is able to successfully delete both .ics link and all deadlines associated with the .ics link
   </td>
   <td>

<p id="gdcalert54" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image54.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert55">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image54.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Auto retrieval of .ics data 
   </td>
   <td>Bot should be able to successfully retrieve any new/deleted deadlines from the canvas .ics link associated with the user.
   </td>
   <td>See <strong>{2} [ Function 1 : Assignment Deadlines ]</strong>
<p>
<strong>How does the automatic Canvas Calendar .ics link work?</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Sending reminders of Deadlines
   </td>
   <td>The bot should send a reminder if the deadline is  [ 72 hours , 24 hours , 6 hours , 1 hour , is due ] from the due date
   </td>
   <td>See <strong>{2} [ Function 1 : Assignment Deadlines ]</strong>
<p>
<strong>How does the bot send reminders of approaching deadlines?</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing of multiple pages for >8 valid deadlines
   </td>
   <td>The bot should split the deadlines split to multiple pages when there are >8 valid deadlines, with the buttons next and previous to navigate through the pages
   </td>
   <td>See <strong>{2} [ Function 1 : Assignment Deadlines ]</strong>
<p>
<strong>In the event of more than >8 valid deadlines in the list.</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Auto delete of due deadlines
   </td>
   <td>Deadlines past >24 hours of due date will be auto deleted from the database
   </td>
   <td>NIL
   </td>
   <td>
   </td>
  </tr>
</table>


**Function 2: Personal Planner**


<table>
  <tr>
   <td><strong>Feature</strong>
   </td>
   <td><strong>Expected</strong>
   </td>
   <td><strong>Actual</strong>
   </td>
   <td><strong>Outcome</strong>
   </td>
  </tr>
  <tr>
   <td>Viewing of Personal Planner w/o any valid events
   </td>
   <td>The bot should send the message “Your Personal Planner is currently empty. Please add an event to begin.”
   </td>
   <td>

<p id="gdcalert55" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image55.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert56">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image55.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing of Personal Planner with valid events
   </td>
   <td>The bot should display each event in the format
<p>
<strong>index) title</strong>
<p>
<strong>Date:</strong>
<p>
<strong>Time Left:</strong>
<p>
<strong>Additional Notes:</strong>
   </td>
   <td>

<p id="gdcalert56" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image56.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert57">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image56.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Events are sorted in chronological order
   </td>
   <td>Events with the closest date should be at the top
   </td>
   <td>

<p id="gdcalert57" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image57.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert58">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image57.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Add Events
   </td>
   <td>Bot should be able to accurately add events.
   </td>
   <td>

<p id="gdcalert58" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image58.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert59">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image58.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Delete events
   </td>
   <td>Bot should be able to accurately delete the selected event from the database 
<p>
+ delete selection list should be sorted correctly in chronological order.
   </td>
   <td>

<p id="gdcalert59" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image59.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert60">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image59.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Adding time to event
   </td>
   <td>If valid time in the past is given, the bot should inform the user to enter a future time.
<p>
Elif if an invalid format is given, then the bot will send a more detailed instruction on the valid time format
<p>
Else if a valid time is given, the bot will move on to adding additional notes.
   </td>
   <td>

<p id="gdcalert60" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image60.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert61">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image60.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>For additional notes, the bot accurately adds in the input response by the user. 
   </td>
   <td>
   </td>
   <td>

<p id="gdcalert61" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image61.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert62">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image61.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>If the user chose to “Skip comments” , the bot successfully adds the event while leaving additional notes as an empty string.
   </td>
   <td>
   </td>
   <td>

<p id="gdcalert62" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image62.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert63">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image62.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Events past >24 hours should be auto deleted.
   </td>
   <td>Before loading event list, the bot will check and delete any event past 24 hours its time
   </td>
   <td>NIL
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Reminders are sent for events
   </td>
   <td>The bot will send a reminder if the event is  [ 24 hours , 1 hour , 5 mins , now ] from the event time.
   </td>
   <td>See <strong>{3} [Function 2: Personal Planner]</strong>
<p>
<strong>How does the bot send reminders of approaching events?</strong>
   </td>
   <td>
   </td>
  </tr>
</table>


**Function 3: School Timetable**


<table>
  <tr>
   <td><strong>Feature</strong>
   </td>
   <td><strong>Expected</strong>
   </td>
   <td><strong>Actual</strong>
   </td>
   <td><strong>Outcome</strong>
   </td>
  </tr>
  <tr>
   <td>Viewing timetable for configured lessons
   </td>
   <td>Bot should fetch configured lessons and display them
   </td>
   <td>See <strong>Figure 4.8</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Configuring of lessons with valid lesson slot number provided
   </td>
   <td>Lesson should be configured and status will be changed
   </td>
   <td>See <strong>Figure 4.4</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Unconfiguring of lessons
   </td>
   <td>Lesson should be changed to unconfigured and Users can choose to configure them again
   </td>
   <td>See <strong>Figure 4.6</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing timetable when no modules are added
   </td>
   <td>Bot will inform User and prompt them to add modules
   </td>
   <td>

<p id="gdcalert63" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image63.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert64">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image63.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Adding a new module to User’s list
   </td>
   <td>Lessons should turn up as unconfigured and Users have the option to configure them
   </td>
   <td>NIL
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Deleting a module from User’s list
   </td>
   <td>Lessons and related data from weekly timetable are deleted
   </td>
   <td>NIL
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing lessons with no configured lessons
   </td>
   <td>Bot should inform User that there are no lessons left for the week
   </td>
   <td>See <strong>Figure 4.1 and 4.2</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Configure lesson and User provides invalid lesson slot number
   </td>
   <td>Bot will inform User and prompt to try again or report issue
   </td>
   <td>

<p id="gdcalert64" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image64.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert65">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image64.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Unconfigure lesson but User does not have any configured lessons
   </td>
   <td>Bot will inform User and prompt to configure lessons
   </td>
   <td>See <strong>Figure 4.7</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Ignore and view timetable
   </td>
   <td>Bot should only show configured lessons to the User
   </td>
   <td>NIL
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing timetable in new week
   </td>
   <td>Bot should generate and fetch new timetable when week changes
   </td>
   <td>NIL
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing timetable during recess week
   </td>
   <td>Bot should inform User that it is recess week
   </td>
   <td>

<p id="gdcalert65" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image65.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert66">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image65.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing timetable during reading week
   </td>
   <td>Bot should inform User that it is reading week
   </td>
   <td>

<p id="gdcalert66" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image66.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert67">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image66.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing timetable during examination period
   </td>
   <td>Bot should inform User that it is examinations and there are no more lessons
   </td>
   <td>

<p id="gdcalert67" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image67.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert68">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image67.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing timetable when semester has ended
   </td>
   <td>Bot should inform User that semester has ended
   </td>
   <td>

<p id="gdcalert68" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image68.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert69">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image68.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing timetable in the middle of the week
   </td>
   <td>Lessons that have occurred will not be shown
   </td>
   <td>NIL
   </td>
   <td>
   </td>
  </tr>
</table>


**Function 4: Exam Timetable**


<table>
  <tr>
   <td><strong>Feature</strong>
   </td>
   <td><strong>Expected</strong>
   </td>
   <td><strong>Actual</strong>
   </td>
   <td><strong>Outcome</strong>
   </td>
  </tr>
  <tr>
   <td>Adding a module
   </td>
   <td>Exam timings (if any) of added module should be displayed
   </td>
   <td>See <strong>Figure 5.1</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Deleting a module
   </td>
   <td>Exam timings (if any) of deleted module will no longer be displayed
   </td>
   <td>NIL
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing of past exams
   </td>
   <td>Exams that have already taken place will not be shown
   </td>
   <td>NIL
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing of exam countdown
   </td>
   <td>Countdown of days to exam 
<p>
+  Detect any exam clash
   </td>
   <td>See <strong>Figure 5.1</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Viewing of exams with no modules added
   </td>
   <td>User is informed and prompted to add module
   </td>
   <td>

<p id="gdcalert69" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image69.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert70">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image69.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
</table>


**Function 5: View Modules (Add/Delete)**


<table>
  <tr>
   <td><strong>Feature</strong>
   </td>
   <td><strong>Expected</strong>
   </td>
   <td><strong>Actual</strong>
   </td>
   <td><strong>Outcome</strong>
   </td>
  </tr>
  <tr>
   <td>View modules when User has no modules
   </td>
   <td>User will be informed and prompted to add modules
   </td>
   <td>

<p id="gdcalert70" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image70.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert71">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image70.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Invalid module code when adding module
   </td>
   <td>User will be informed and prompted to try again
   </td>
   <td>See <strong>Figure 6.4</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Module already added when User adding module
   </td>
   <td>User will be informed and returned to View Modules Main page
   </td>
   <td>See <strong>Figure 6.5</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>User has no modules when deleting module
   </td>
   <td>User will be informed and prompted to add modules
   </td>
   <td>

<p id="gdcalert71" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image71.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert72">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image71.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Deleting of module in User’s list
   </td>
   <td>User informed of successful deletion
   </td>
   <td>See <strong>Figure 6.7</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Valid module code when adding module
   </td>
   <td>User informed of successful adding
   </td>
   <td>See <strong>Figure 6.3</strong>
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>User view added modules
   </td>
   <td>Bot should fetch added modules and display them
   </td>
   <td>

<p id="gdcalert72" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image72.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert73">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image72.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
</table>


**Function 6: Report Issues**


<table>
  <tr>
   <td><strong>Feature</strong>
   </td>
   <td><strong>Expected</strong>
   </td>
   <td><strong>Actual</strong>
   </td>
   <td><strong>Outcome</strong>
   </td>
  </tr>
  <tr>
   <td>Reporting of bugs or giving feedback
   </td>
   <td>The is able to discern whether the user is reporting a bug or want to give feedback
   </td>
   <td>

<p id="gdcalert73" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image73.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert74">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image73.png" width="" alt="alt_text" title="image_tooltip">

<p>


<p id="gdcalert74" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image74.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert75">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image74.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Confirmation of Report
   </td>
   <td>The bot will send the user their input and ask whether they wish to confirm and send the report.
   </td>
   <td>

<p id="gdcalert75" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image75.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert76">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image75.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Edit of Report
   </td>
   <td>The user may choose to edit, and the bot should delete the previous input and successfully update the new input report from the users.
   </td>
   <td>

<p id="gdcalert76" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image76.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert77">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image76.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Storing of reports in database
   </td>
   <td>The bot should be able to store the data with the report, username, time reported successfully, while able to distinguish whether the report was a bug report or feedback
   </td>
   <td>

<p id="gdcalert77" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image77.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert78">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image77.png" width="" alt="alt_text" title="image_tooltip">


<p id="gdcalert78" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image78.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert79">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


<img src="images/image78.png" width="" alt="alt_text" title="image_tooltip">

   </td>
   <td>
   </td>
  </tr>
</table>


**<span style="text-decoration:underline;">User Testing:</span>**

**<span style="text-decoration:underline;">Interviewee 1 </span>**

**<span style="text-decoration:underline;"> \
</span>Profile:** Male 17 Year Old Student at Nanyang Polytechnic, Year 1 Foundation Polytechnic Programme

**Q: “Could you share how you have been using the bot? How effective has the bot been in helping you better manage your deadlines?”**

A: “I have been using the bot for assignment plans and test timing. It has been effective in informing me on the dates and the time left which helped me better plan and be more aware of my assignments. It also helps me reduce procrastination and I have a clearer picture of the time I actually have left and switch my mood to be more focused.”

**Q: “Taking into consideration as a non-NUS student, are there any pain points you identify with using our bot? (For example any issues with UI, any bugs you faced etc.)**

A: “Don’t particularly see any major bugs, but when the server resets there are issues that arise but are very minor. Sometimes the bot may just crash but restarting with calling /start once again gets it back up, so it's a rather easy fix but best if this issue does not occur when using the bot.”

**Q:”Overall, how satisfied are you with the accuracy and reliability of the deadlines recorded by the bots. Has it overall helped you manage your deadlines better? ”**

A: “Yes, as mentioned in the 1st question, it has helped me better manage my time since my poly portal can be rather messy. The special feature of the bot i would say is displaying the actual time left, and this is why i preferred the bot over using my calendar application (which only displays the date and not time left)”

**Q: “Any final thing you want to add on? It can be suggestions or the overall opinion of the bot.**”

A: “The bot has achieved its intended purposes and does it quite well, there is not much to suggest except that it is quite useful for me to use in my studies. Preferably, I would hope that the bot can also be integrated with my school system, like how you used the bot to integrate with NUS modules. For features, maybe adding a daily to-do list to the bot will help me better manage my assignments better, as I am currently using notion to do it.”

**<span style="text-decoration:underline;">Comments: </span>**Despite not being an NUS student, some functions are not usable. However, the user enjoys the bot and I am glad that it has helped him better manage his assignments. He particularly enjoyed that the bot is not too overly complex and is conveniently on telegram, which is why he overall enjoys and is using the bot for his schooling. -Chester

**<span style="text-decoration:underline;">Milestone 3</span>**

**<span style="text-decoration:underline;">Milestone 3: Development Plan</span>**



* Configuring the database
1. Importing and extracting of class data from nusmods calendar .ics file
2. Restructuring some data storing and retrieval algorithm to improve speed
* Improve Quality of Life for functions
1. Using imported class data from nusmods calendar .ics file, the bot automatically configures the lesson users are taking, hence users need not manually add in.
2. For School Timetable, allow users to delete all existing configured lessons.
3. Include warning for exam clash in View examinations.

**<span style="text-decoration:underline;">Milestone 3: Evaluation</span>**

One main focus on Milestone 3 was to implement the function which allows users to upload their .ics data file from nusmods and then upload it onto the bot, then automatically configuring the lessons for the users. This is welcomed as it removes the need to manually configure every lesson to generate the timetable. We also did some restructuring of the database to extract and store data more consistently, which should help improve speed. The bot hosting on Replit is still somewhat reliable in terms of uptime, however some issues faced were mostly due to the bot not handling next step registers properly and hence result in some users not receiving response from the bot.

**<span style="text-decoration:underline;">Milestone 2 (Archived)</span>**

**<span style="text-decoration:underline;">Milestone 2: Development Plan</span>**



* Configuring the database
3. Importing of data from Canvas Calendar to auto-fill entries in Assignment Deadlines
4. Import data such as exam timing and import timetable from NUSMods
5. Establishing front-end hosting for the bot, currently the server is locally hosted, but the bot's functions are working back-end.
1. Decide on a hosting service to deploy the bot (Replit)
* Improve Quality of Life for functions
4. For Assignment Deadlines and Personal Planner, automatically deletes entries 24 hours past the due dates. (Currently user need to manually delete)
5. For Assignment Deadlines and personal planner, the bot will send reminders in intervals to remind users of the approaching deadline/event time.
6. For School Timetable, allow users to delete existing configured lessons
7. Include countdown timer for final exam dates in Exam Time Table function
8. Display dates alongside with the days of the week in School Timetable function

**<span style="text-decoration:underline;">Milestone 2: Evaluation</span>**

Carrying on from Milestone 1, we have made multiple QOL changes to make the UI more friendly. One main feature of our bot, which is the ability to integrate canvas calendar data to automate a deadline planner list for us, but it's hard to effectively test how useful it is as it is currently in semester break, but it is currently looking fine with mock data. We have also better organized our database and changed some algorithms to improve the bot speed. For Milestone 3, we will further make more QOL updates, and we will test out more features to implement in our bot.

In addition, we are using Replit to host the bot, however we will not provide the replit link for security reasons. 

**<span style="text-decoration:underline;">Milestone 1 (Archived)</span>**

**<span style="text-decoration:underline;">Milestone 1: Development Plan</span>**

**2nd week of May:**

Finalized poster and video for Orbital Lift-off

Started to read up on the necessary technologies: pyTelegramAPI Python package, Firebase storage, hosting services, Git and Github

**3rd week of May:**

Gradual application of technologies learnt the week before

Creating GitHub Repo and discussed on how to collaborate

Creating of Firebase database and initializing it in script

Coding of the main menu of the bot

**4th week of May:**

Testing the bots and finalize documentation for Milestone 1 Submission

**Chester: **Coded the following functions. Assignment Deadlines, Personal Planner and Report Issues

**Zhi Chao: **Coded the following functions. School Timetable, Exam Timetable and View Modules

**<span style="text-decoration:underline;">Milestone 1: Evaluation</span>**

Plan and design the user interactions with the Telegram Bot such as



1. Editing the personal planner (Adding/Removing events)
2. View and edit the modules they are taking
3. View due date for assignments
4. View upcoming assignments and due dates
5. View schedule for school and exam
6. Reporting of errors to admin
7. Establishing a database to store user’s data
8. Admin functions - Viewing of issues reported by users

For Milestone 1, we will be focused on the technical proof of the bot, by ensuring that the bot is able to fetch and call functions upon a given command. We will also do some testing with NUSMods API to extract the database of the modules offered in NUS, which we will use to help establish user’s establish their module profile.

**NOTE:**

Database is functional and implemented for all functions. Backend is working but it is yet to be hosted on any server as we are still exploring hosting options such as Replit, Heroku, Firebase etc.

**Additional Information**



1. **Regarding Canvas .ics link**

Since it is the** semester break**, there **are no assigned assignments available** at all in canvas. From my understanding through testing, data in the canvas calendar will **only be valid if the assignment time is in the future** (meaning not due). There could be **rare cases** where some past assignments from the previous semester are ‘**still active’ (despite being past it due date)**, and could** cause an error loading **the assignment deadlines list, if that is the case** please manually delete that assignment** (shouldn’t be an issue as almost all 22/23 Sem 2 modules pages are already deleted). **To do testing for this feature, you may go to your own canvas calendar, click on the plus button and add in your own mock assignments** (e.g Milestone 2 26/06/2023 1400hrs and Milestone 3 24/07/2023 1400hrs). It is also **advisable not to add any event with dates from the past**, as the **above mentioned error may occur** **(although the bot is still able to auto delete any assignments past 24 hours the due date)**

**If you happen to face this error and thus are unable to open the assignment deadlines list, one fix is to delete your data from the database. You may do so by typing ‘delete_self’ manually in the main menu and your user data will be reseted. **



2. **Regarding NUSMods updating of AY23/24 Sem 1 data**

NUSMods have updated AY23/24 data on 23 June, 3 days before the M2 deadline. We have imported AY23/24 data and so far it seemingly works fine, however due to the **expected changes in the class and exam timing** of modules since it is not confirmed, there could be cases where the bot **displays incorrect information or outdated timing**. The bot is currently set to fetch AY23/24 Sem 1 data and there shouldn’t be any issues, and newly added mods are also able to be fetched. The functions should be working but if you do face any issues,** please recalibrate your modules/lessons** so that it will **retrieve the updated data** from NUSMods.

**You** **may reach out to us on Telegram @angchester or @lzc_88 , or use the Report Issues function in the bot if you have any issues or feedback.**
