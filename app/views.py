from flask import render_template, flash, redirect, session, request, url_for
from hashtagify import Hashtagify
from app import app
from config import DEFAULT_TITLE, DEFAULT_CONTENT


@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		session['Hashtagify'] = None
		try:
			form_data = request.form
			title = form_data.get('title', None)
			content = form_data.get('content', None)
			ht = Hashtagify(title, content.encode('utf8'))
			session['Hashtagify'] = {'title': title, 'content': content}

			return redirect(url_for('functions'))
		except Exception, e:
			flash(unicode(e), 'error')

	return render_template("index.html", title='Index', default_title=DEFAULT_TITLE, default_content=DEFAULT_CONTENT)

@app.route("/functions", methods=["GET", "POST"])
def functions():
	ht_data = session.get('Hashtagify', None)
	if ht_data is None:
		flash("Hashtagify instance doesn't exist", 'error')

		return redirect(url_for('index'))

	if request.method == "POST":
		try:
			form_data = request.form

			token = form_data.get('token', None)
			t_sentence = form_data.get('t_sentence', None)
			sentence = form_data.get('sentence', None)
			is_title = form_data.get('is_title', False)
			text = form_data.get('text', None)
			t1 = form_data.get('t1', None)
			t2 = form_data.get('t2', None)
			ratio = form_data.get('ratio', None)

			title = ht_data.get('title', None)
			content = ht_data.get('content', None)
			ht = Hashtagify(title, content.encode('utf8'))
			session['Hashtagify'] = {'title': title, 'content': content}

			if token is not None:
				session['token'] = token
				stem = ht.stem(token)
				return render_template("functions.html", title='Functions', stem=stem if stem is not None else 'None')

			if t_sentence is not None:
				session['t_sentence'] = t_sentence
				tokenize_sentence = ht.tokenize_sentence(t_sentence)
				return render_template("functions.html", title='Functions', tokenize_sentence=tokenize_sentence if tokenize_sentence is not None else 'None')

			if sentence is not None:
				session['sentence'] = sentence
				session['is_title'] = is_title
				add_sentence_to_index = ht.add_sentence_to_index(sentence, bool(is_title))
				return render_template("functions.html", title='Functions', add_sentence_to_index_form=add_sentence_to_index if add_sentence_to_index is not None else 'None')

			if text is not None:
				session['text'] = text
				build_index = ht.build_index(text)
				return render_template("functions.html", title='Functions', build_index=build_index if build_index is not None else 'None')

			if t1 and t2 is not None:
				session['t1'] = t1
				session['t2'] = t2
				merge_words = ht.merge_words(t1, t2)
				return render_template("functions.html", title='Functions', merge_words=merge_words if merge_words is not None else 'None')

			if ratio is not None:
				session['ratio'] = ratio
				hashtagify = ht.hashtagify(float(ratio))
				return render_template("functions.html", title='Functions', hashtagify=hashtagify if hashtagify is not None else 'None')

		except Exception, e:
			flash(unicode(e), 'error')

	return render_template("functions.html", title='Functions')