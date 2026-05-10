// @trace TASK-013
import { useState, useEffect, useCallback } from 'react';
import './UserManagement.css';

interface User {
  id: number;
  username: string;
  email: string;
  status: string;
}

export function UserManagement() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const getAuthHeaders = useCallback(() => {
    const token = localStorage.getItem('token') || '';
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };
  }, []);

  const fetchUsers = useCallback(async () => {
    try {
      // loading is already true initially
      const response = await fetch('/admin/users', {
        headers: getAuthHeaders()
      });
      if (!response.ok) {
        throw new Error('Failed to fetch users. Make sure you are logged in as admin.');
      }
      const data = await response.json();
      setUsers(data.users || []);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setLoading(false);
    }
  }, [getAuthHeaders]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchUsers();
  }, [fetchUsers]);

  const handleStatusChange = async (userId: number, newStatus: string) => {
    try {
      const response = await fetch(`/admin/users/${userId}/status`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ status: newStatus }),
      });

      if (!response.ok) {
        throw new Error('Failed to update status');
      }

      const data = await response.json();
      setUsers(users.map(u => (u.id === userId ? { ...u, status: data.status } : u)));
    } catch (err) {
      if (err instanceof Error) {
        alert(`Error updating user: ${err.message}`);
      } else {
        alert('An unknown error occurred updating user');
      }
    }
  };

  if (loading) return <div className="user-management-loading">Loading users...</div>;
  if (error) return <div className="user-management-error">Error: {error}</div>;

  return (
    <div className="user-management">
      <h2>User Management Dashboard</h2>
      <table className="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>
                <span className={`status-badge ${user.status === 'active' ? 'active' : 'blocked'}`}>
                  {user.status}
                </span>
              </td>
              <td>
                <select 
                  value={user.status}
                  onChange={(e) => {
                    if (e.target.value !== user.status) {
                      handleStatusChange(user.id, e.target.value);
                    }
                  }}
                  className="action-select"
                >
                  <option value="active">Active</option>
                  <option value="blocked">Blocked</option>
                </select>
              </td>
            </tr>
          ))}
          {users.length === 0 && (
            <tr>
              <td colSpan={5} className="empty-state">No users found.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
