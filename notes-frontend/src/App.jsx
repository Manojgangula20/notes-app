import { useState, useEffect } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

function App() {
  const [token, setToken] = useState("");
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("secret123");
  const [notes, setNotes] = useState([]);
  const [selectedNote, setSelectedNote] = useState(null);
  const [noteTitle, setNoteTitle] = useState("");
  const [noteContent, setNoteContent] = useState("");
  const [versions, setVersions] = useState([]);

  async function register() {
    await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    // silently ignore 400 Email already registered
  }

  async function login() {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username: email, password }),
    });
    if (!res.ok) return;
    const data = await res.json();
    setToken(data.access_token);
  }

  async function loadNotes() {
    const res = await fetch(`${API_BASE}/notes`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) return;
    const data = await res.json();
    setNotes(data);
  }

  useEffect(() => {
    if (token) loadNotes();
  }, [token]);

  async function selectNote(note) {
    setSelectedNote(note);
    setNoteTitle(note.title);
    setNoteContent(note.content);
    const res = await fetch(`${API_BASE}/notes/${note.id}/versions`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) return;
    setVersions(await res.json());
  }

  async function createNote() {
    const res = await fetch(`${API_BASE}/notes`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title: noteTitle, content: noteContent }),
    });
    if (!res.ok) return;
    setNoteTitle("");
    setNoteContent("");
    await loadNotes();
  }

  async function updateNote() {
    if (!selectedNote) return;
    const res = await fetch(`${API_BASE}/notes/${selectedNote.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title: noteTitle, content: noteContent }),
    });
    if (!res.ok) return;
    await loadNotes();
    await selectNote(selectedNote);
  }

  async function restoreVersion(versionNumber) {
    if (!selectedNote) return;
    const res = await fetch(
      `${API_BASE}/notes/${selectedNote.id}/versions/${versionNumber}/restore`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    if (!res.ok) return;
    await loadNotes();
    await selectNote(selectedNote);
  }

  return (
    <div style={{ display: "flex", gap: "2rem", padding: "1rem" }}>
      <div style={{ width: "250px" }}>
        <h2>Auth</h2>
        <input
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button onClick={register}>Register</button>
        <button onClick={login}>Login</button>
        {token && <p>Logged in.</p>}

        <h2>Notes</h2>
        <button onClick={loadNotes} disabled={!token}>
          Refresh notes
        </button>
        <ul>
          {notes.map(n => (
            <li key={n.id}>
              <button onClick={() => selectNote(n)}>{n.title}</button>
            </li>
          ))}
        </ul>
      </div>

      <div style={{ flex: 1 }}>
        <h2>{selectedNote ? "Edit note" : "New note"}</h2>
        <input
          style={{ width: "100%", marginBottom: "0.5rem" }}
          placeholder="Title"
          value={noteTitle}
          onChange={e => setNoteTitle(e.target.value)}
        />
        <textarea
          style={{ width: "100%", height: "150px" }}
          placeholder="Content"
          value={noteContent}
          onChange={e => setNoteContent(e.target.value)}
        />
        <div>
          <button onClick={createNote} disabled={!token}>
            Create
          </button>
          <button onClick={updateNote} disabled={!token || !selectedNote}>
            Update
          </button>
        </div>

        {selectedNote && (
          <>
            <h3>Version history</h3>
            <ul>
              {versions.map(v => (
                <li key={v.id}>
                  v{v.version}{" "}
                  <button onClick={() => restoreVersion(v.version)}>
                    Restore
                  </button>
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
