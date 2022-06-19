package models

import (
	"errors"
	"time"

	"github.com/google/uuid"
	_ "github.com/mattn/go-sqlite3"
)

type Post struct {
	ID        uuid.UUID `json:"id,omitempty"`
	Author    User      `json:"author"`
	Title     string    `json:"title"`
	Content   string    `json:"content"`
	Thumbnail string    `json:"thumbnail,omitempty"`
	CreatedAt time.Time `json:"created_at,omitempty"`
	UpdatedAt time.Time `json:"updated_at,omitempty"`
}

func (p *Post) GetAll() ([]Post, error) {
	db := GetConnection()
	q := `SELECT posts.id, posts.title, posts.content, posts.thumbnail, posts.created_at, posts.updated_at,
			users.id as author_id, users.username as author_username, users.email as author_email,
			users.hashed_password as author_hashed_password, users.created_at as author_created_at,
			users.updated_at as author_updated_at FROM posts JOIN users ON posts.author_id=users.id`
	rows, err := db.Query(q)
	if err != nil {
		return []Post{}, err
	}
	defer rows.Close()

	author := User{}
	posts := []Post{}
	for rows.Next() {
		rows.Scan(
			&p.ID,
			&p.Title,
			&p.Content,
			&p.Thumbnail,
			&p.CreatedAt,
			&p.UpdatedAt,
			&author.ID,
			&author.Username,
			&author.Email,
			&author.HashedPassword,
			&author.UpdatedAt,
			&author.CreatedAt,
		)
		p.Author = author
		posts = append(posts, *p)
	}
	return posts, nil
}

func (p *Post) GetByID(ID string) (Post, error) {
	db := GetConnection()
	q := `SELECT posts.id, posts.title, posts.content, posts.thumbnail, posts.created_at, posts.updated_at,
			users.id as author_id, users.username as author_username, users.email as author_email,
			users.hashed_password as author_hashed_password, users.created_at as author_created_at,
			users.updated_at as author_updated_at, users.is_admin as author_is_admin FROM posts JOIN users ON posts.author_id=users.id
			WHERE posts.id = ?`
	rows, err := db.Query(q, ID)
	if err != nil {
		return Post{}, err
	}
	defer rows.Close()

	author := User{}
	rows.Next()
	rows.Scan(
		&p.ID,
		&p.Title,
		&p.Content,
		&p.Thumbnail,
		&p.CreatedAt,
		&p.UpdatedAt,
		&author.ID,
		&author.Username,
		&author.Email,
		&author.HashedPassword,
		&author.UpdatedAt,
		&author.CreatedAt,
		&author.IsAdmin,
	)
	p.Author = author

	return *p, nil
}

func (p Post) Create() error {
	db := GetConnection()

	q := `INSERT INTO posts (id, author_id, title, content, thumbnail, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?, ?)`

	stmt, err := db.Prepare(q)
	if err != nil {
		return err
	}

	defer stmt.Close()

	r, err := stmt.Exec(p.ID, p.Author.ID, p.Title, p.Content, p.Thumbnail, time.Now(), time.Now())
	if err != nil {
		return err
	}

	if i, err := r.RowsAffected(); err != nil || i != 1 {
		return errors.New("ERROR: Expected one row modified")
	}

	return nil
}

func (p Post) Update() error {
	db := GetConnection()
	q := `UPDATE posts set author_id=?, title=?, content=?, thumbnail=?, updated_at=?
            WHERE id=?`
	stmt, err := db.Prepare(q)
	if err != nil {
		return err
	}
	defer stmt.Close()

	r, err := stmt.Exec(p.Author.ID, p.Title, p.Content, p.Thumbnail, time.Now(), p.ID)
	if err != nil {
		return err
	}

	if i, err := r.RowsAffected(); err != nil || i != 1 {
		return errors.New("ERROR: Expected one row modified")
	}

	return nil
}