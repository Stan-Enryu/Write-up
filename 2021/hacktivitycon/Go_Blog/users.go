package models

import (
	"crypto/sha512"
	"encoding/hex"
	"errors"
	"time"

	"github.com/google/uuid"
	_ "github.com/mattn/go-sqlite3"
)

type User struct {
	ID             uuid.UUID `json:"id,omitempty"`
	Username       string    `json:"username"`
	Password       string    `json:"password,omitempty"`
	HashedPassword string    `json:"hashed_password,omitempty"`
	Email          string    `json:"email"`
	IsAdmin        bool      `json:"is_admin"`
	CreatedAt      time.Time `json:"created_at,omitempty"`
	UpdatedAt      time.Time `json:"updated_at,omitempty"`
}

func (u *User) GetAll() ([]User, error) {
	db := GetConnection()
	q := `SELECT
            id, username, email, hashed_password, is_admin, created_at, updated_at
            FROM users`
	rows, err := db.Query(q)
	if err != nil {
		return []User{}, err
	}
	defer rows.Close()

	users := []User{}
	for rows.Next() {
		rows.Scan(
			&u.ID,
			&u.Username,
			&u.Email,
			&u.HashedPassword,
			&u.IsAdmin,
			&u.CreatedAt,
			&u.UpdatedAt,
		)
		users = append(users, *u)
	}
	return users, nil
}

func (u User) Create() error {
	db := GetConnection()

	q := `INSERT INTO users (id, username, email, hashed_password, is_admin, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?, ?)`

	stmt, err := db.Prepare(q)
	if err != nil {
		return err
	}

	defer stmt.Close()

	h := sha512.New()
	h.Write([]byte(u.Password))

	r, err := stmt.Exec(u.ID, u.Username, u.Email, hex.EncodeToString(h.Sum(nil)), u.IsAdmin, time.Now(), time.Now())
	if err != nil {
		return err
	}

	if i, err := r.RowsAffected(); err != nil || i != 1 {
		return errors.New("ERROR: Expected one row modified")
	}

	return nil
}

func (u User) Update() error {
	db := GetConnection()
	q := `UPDATE users set username=?, email=?, is_admin=?, updated_at=? 
            WHERE id=?`
	stmt, err := db.Prepare(q)
	if err != nil {
		return err
	}
	defer stmt.Close()

	r, err := stmt.Exec(u.Username, u.Email, u.IsAdmin, time.Now(), u.ID)
	if err != nil {
		return err
	}

	if i, err := r.RowsAffected(); err != nil || i != 1 {
		return errors.New("ERROR: Expected one row modified")
	}

	return nil
}

func (u User) ChangePassword(newPassword string) error {
	db := GetConnection()
	q := `UPDATE users set hashed_password=?
            WHERE id=?`
	stmt, err := db.Prepare(q)
	if err != nil {
		return err
	}
	defer stmt.Close()

	h := sha512.New()
	h.Write([]byte(newPassword))

	r, err := stmt.Exec(hex.EncodeToString(h.Sum(nil)), u.ID)
	if err != nil {
		return err
	}

	if i, err := r.RowsAffected(); err != nil || i != 1 {
		return errors.New("ERROR: Expected one row modified")
	}

	return nil
}

func (u *User) GetByUsername(username string) (User, error) {
	db := GetConnection()
	q := `SELECT
            id, username, email, hashed_password, is_admin, created_at, updated_at
            FROM users WHERE username=?`
	rows, err := db.Query(q, username)
	if err != nil {
		return User{}, err
	}
	defer rows.Close()

	rows.Next()
	rows.Scan(
		&u.ID,
		&u.Username,
		&u.Email,
		&u.HashedPassword,
		&u.IsAdmin,
		&u.CreatedAt,
		&u.UpdatedAt,
	)

	return *u, nil
}

func (u *User) GetByEmail(email string) (User, error) {
	db := GetConnection()
	q := `SELECT
            id, username, email, hashed_password, is_admin, created_at, updated_at
            FROM users WHERE email=?`
	rows, err := db.Query(q, email)
	if err != nil {
		return User{}, err
	}
	defer rows.Close()

	rows.Next()
	rows.Scan(
		&u.ID,
		&u.Username,
		&u.Email,
		&u.HashedPassword,
		&u.IsAdmin,
		&u.CreatedAt,
		&u.UpdatedAt,
	)

	return *u, nil
}

func (u *User) GetByID(ID string) (User, error) {
	db := GetConnection()
	q := `SELECT
            id, username, email, hashed_password, is_admin, created_at, updated_at
            FROM users WHERE id=?`
	rows, err := db.Query(q, ID)
	if err != nil {
		return User{}, err
	}
	defer rows.Close()

	rows.Next()
	rows.Scan(
		&u.ID,
		&u.Username,
		&u.Email,
		&u.HashedPassword,
		&u.IsAdmin,
		&u.CreatedAt,
		&u.UpdatedAt,
	)

	return *u, nil
}

func (u *User) CheckPassword(password string) bool {
	h := sha512.New()
	h.Write([]byte(password))
	return u.HashedPassword == hex.EncodeToString(h.Sum(nil))
}