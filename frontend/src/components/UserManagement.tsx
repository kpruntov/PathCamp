// @trace TASK-013
import { useState, useEffect, useCallback } from 'react';

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

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-fantasy-accent text-xl animate-pulse">Loading users...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 max-w-4xl mx-auto mt-10 bg-fantasy-danger/20 border border-fantasy-danger text-fantasy-text rounded-md shadow-md">
        <h3 className="font-bold text-lg mb-2 text-fantasy-danger">Error Loading Users</h3>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-8 max-w-6xl mx-auto">
      <div className="mb-8 border-b-2 border-fantasy-accent pb-4 flex items-center justify-between">
        <h2 className="text-3xl font-bold text-fantasy-accent drop-shadow-md">
          User Management Dashboard
        </h2>
        <span className="text-sm bg-fantasy-card px-3 py-1 rounded-full shadow-inner border border-fantasy-accent/30">
          Admin View
        </span>
      </div>

      <div className="bg-fantasy-card rounded-lg shadow-lg border border-fantasy-accent/20 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-fantasy-dark/50 text-fantasy-accent uppercase text-sm tracking-wider border-b border-fantasy-accent/20">
                <th className="py-4 px-6 font-semibold">ID</th>
                <th className="py-4 px-6 font-semibold">Username</th>
                <th className="py-4 px-6 font-semibold">Email</th>
                <th className="py-4 px-6 font-semibold">Status</th>
                <th className="py-4 px-6 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-fantasy-dark/50">
              {users.map(user => (
                <tr key={user.id} className="hover:bg-fantasy-dark/30 transition-colors duration-150">
                  <td className="py-4 px-6 font-medium">{user.id}</td>
                  <td className="py-4 px-6 font-bold">{user.username}</td>
                  <td className="py-4 px-6 text-fantasy-text/80">{user.email}</td>
                  <td className="py-4 px-6">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide
                      ${user.status === 'active' 
                        ? 'bg-fantasy-success/20 text-fantasy-success border border-fantasy-success/30' 
                        : 'bg-fantasy-danger/20 text-fantasy-danger border border-fantasy-danger/30'}`}
                    >
                      {user.status}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-right">
                    <select 
                      value={user.status}
                      onChange={(e) => {
                        if (e.target.value !== user.status) {
                          handleStatusChange(user.id, e.target.value);
                        }
                      }}
                      className="bg-fantasy-dark border border-fantasy-accent/30 text-fantasy-text text-sm rounded focus:ring-fantasy-accent focus:border-fantasy-accent block w-full p-2 outline-none shadow-sm cursor-pointer"
                    >
                      <option value="active" className="bg-fantasy-card">Active</option>
                      <option value="blocked" className="bg-fantasy-card">Blocked</option>
                    </select>
                  </td>
                </tr>
              ))}
              {users.length === 0 && (
                <tr>
                  <td colSpan={5} className="py-12 text-center text-fantasy-text/60 italic">
                    No users found. The realm is empty.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}