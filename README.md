<h3>Prerequisite:</h3>
<ol>
<li>Python 3.6 or above installed</li>
<li>pip installed</li>
</ol>
<h3>How to run this project?</h3>
<ol>
<li>Clone or download this repository.</li>
<li>Open terminal in project's directory</li>
<li>Install dependencies with the command <code>pip install -r requirements.txt</code></li>
<li>Take <code>.env</code> from the back-end branch person</li>
<li>Save that <code>.env</code> file in <code>anonymous_social_question_answer/</code> folder</li>
<li>Run command <code>python manage.py migrate
</code> to create database and save all application settings into the database.</li>
<li>Run command <code>python manage.py makemigrations</code> to mark all models/tables into the database</li>
<li>Run command <code>python manage.py migrate
</code> again to confirm changes written in database.</li>
<li>Run command <code>python manage.py runserver</code> and open http://localhost:8000 on your machine's browser.</li>
<li>(Optional) If you want to create your admin account to manage the site. Run command <code>python manage.py createsuperuser</code> and enter all valid credentials it asks you to enter. Then visit http://localhost:8000/admin from your browser it will take you yo admin panel.</li>
</ol>

API Endpoints availble:
<li><code>/api/fetch_posts/page_number(integer)</code></li>
<li><code>/api/vote_post/post_id(integer)</code></li>
<li> <code>/api/report_post/post_id(integer)</code></li>
<li><code>/api/vote_answer/answer_id(integer) </code></li>
<li><code>/api/save/post_id(integer)</code></li>
<li><code>/api/fetch_user_posts/username(string)/page_number(integer)</code></li>
<li><code>/api/delete_answer/answer_id(integer)</code></li>
<li><code>/api/fetch_post_answers/post_id(integer)/page_number(integer)</code></li>
<li><code>/api/fetch_saved_posts/page_number(integer)</code></li>
<li><code>/api/report_answer/answer_id(integer)</code></li>
<li><code>/api/fetch_search_result/query(string)/page_number(integer)</code></li>
<li><code>/api/fetch_by_tag/tag(string)/page_number(integer)</code></li>
<li><code>/api/report_account/account_id(integer)</code></li>
