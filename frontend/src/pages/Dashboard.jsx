import { useEffect, useState } from 'react';
import {
  PlusCircle,
  Folder,
  CheckSquare,
  LogOut,
  LayoutDashboard,
  Search,
  MoreVertical,
  Calendar,
  Clock,
  ExternalLink,
  X,
  AlertCircle
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('tasks');
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [showTaskModal, setShowTaskModal] = useState(false);
  const [showProjectModal, setShowProjectModal] = useState(false);

  // Form states
  const [taskForm, setTaskForm] = useState({ title: '', description: '', project: '', status: 'new' });
  const [projectForm, setProjectForm] = useState({ name: '', description: '' });
  const [formError, setFormError] = useState('');

  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      const [projectsRes, tasksRes] = await Promise.all([
        api.get('/projects/').catch(e => ({ data: [] })),
        api.get('/tasks/').catch(e => ({ data: [] }))
      ]);
      setProjects(Array.isArray(projectsRes.data) ? projectsRes.data : []);
      setTasks(Array.isArray(tasksRes.data) ? tasksRes.data : (tasksRes.data?.results || []));
    } catch (err) {
      console.error('Fetch error', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  const createTask = async (e) => {
    e.preventDefault();
    setFormError('');
    if (!taskForm.project) {
        setFormError('Пожалуйста, выберите проект');
        return;
    }
    try {
      await api.post('/tasks/', taskForm);
      setShowTaskModal(false);
      setTaskForm({ title: '', description: '', project: '', status: 'new' });
      fetchData();
    } catch (err) {
      setFormError('Ошибка: ' + JSON.stringify(err.response?.data));
    }
  };

  const createProject = async (e) => {
    e.preventDefault();
    setFormError('');
    try {
      await api.post('/projects/', projectForm);
      setShowProjectModal(false);
      setProjectForm({ name: '', description: '' });
      fetchData();
    } catch (err) {
      setFormError('Ошибка: ' + JSON.stringify(err.response?.data));
    }
  };

  const filteredTasks = selectedProjectId
    ? tasks.filter(t => t.project === selectedProjectId)
    : tasks;

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-50 text-slate-900 font-sans">
      <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
      <p className="mt-4 text-slate-500 font-medium tracking-tight">Загрузка данных...</p>
    </div>
  );

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-indigo-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 hidden lg:flex flex-col shrink-0">
        <div className="p-6 border-b border-slate-100 flex items-center gap-3">
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-100">
            <LayoutDashboard size={24} />
          </div>
          <span className="font-bold text-xl text-slate-800 tracking-tight">TaskFlow</span>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          <button
            onClick={() => { setActiveTab('tasks'); setSelectedProjectId(null); }}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${activeTab === 'tasks' && !selectedProjectId ? 'bg-indigo-50 text-indigo-600' : 'text-slate-500 hover:bg-slate-50'}`}
          >
            <CheckSquare size={18} />
            Все задачи
          </button>

          <div className="mt-6 mb-2 px-4 text-[10px] font-black uppercase tracking-[0.2em] text-slate-400">Проекты</div>
          {projects.map(project => (
            <button
                key={project.id}
                onClick={() => { setActiveTab('tasks'); setSelectedProjectId(project.id); }}
                className={`w-full flex items-center justify-between gap-3 px-4 py-3 rounded-xl font-semibold text-sm transition ${selectedProjectId === project.id ? 'bg-indigo-50 text-indigo-600' : 'text-slate-500 hover:bg-slate-50'}`}
            >
                <div className="flex items-center gap-3 truncate">
                    <Folder size={18} />
                    <span className="truncate">{project.name}</span>
                </div>
            </button>
          ))}

          <button
            onClick={() => { setShowProjectModal(true); setFormError(''); }}
            className="w-full flex items-center gap-3 px-4 py-3 text-indigo-600 hover:bg-indigo-50 rounded-xl font-bold text-sm transition mt-2"
          >
            <PlusCircle size={18} />
            Новый проект
          </button>
        </nav>

        <div className="p-4 border-t border-slate-100">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 text-slate-500 hover:text-red-600 hover:bg-red-50 rounded-xl font-semibold text-sm transition text-left"
          >
            <LogOut size={18} />
            Выйти
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Topbar */}
        <header className="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-8 shrink-0 sticky top-0 z-30">
          <div className="relative w-96 max-w-full hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input
              type="text"
              placeholder="Поиск..."
              className="w-full pl-10 pr-4 py-2 bg-slate-100 border-transparent rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500 transition outline-none text-sm"
            />
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => { setShowTaskModal(true); setFormError(''); }}
              className="flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white font-bold text-sm rounded-xl hover:bg-indigo-700 transition shadow-lg shadow-indigo-100 active:scale-95"
            >
              <PlusCircle size={18} />
              Новая задача
            </button>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-auto p-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-black text-slate-800 tracking-tight">
                    {selectedProjectId ? projects.find(p => p.id === selectedProjectId)?.name : 'Все задачи'}
                </h1>
                <p className="text-slate-500 mt-1 font-medium">
                  Найдено <span className="text-indigo-600">{filteredTasks?.length || 0}</span> задач
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-6">
              {/* Tasks List */}
              <div className="space-y-4">
                {filteredTasks.length === 0 ? (
                <div className="bg-white rounded-[2.5rem] p-16 text-center border-2 border-dashed border-slate-200">
                    <CheckSquare size={48} className="text-slate-200 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-slate-800">Задач нет</h3>
                    <p className="text-slate-400 mt-2 font-medium">Похоже, в этом разделе пока пусто.</p>
                </div>
                ) : (
                filteredTasks.map(task => (
                    <div key={task.id} className="group bg-white p-6 rounded-3xl border border-transparent hover:border-indigo-100 hover:shadow-2xl hover:shadow-indigo-100/30 transition duration-500 flex items-start gap-5">
                    <div className={`mt-1 h-12 w-12 shrink-0 rounded-2xl flex items-center justify-center transition group-hover:scale-110 duration-500 ${
                        task.status === 'done' ? 'bg-green-50 text-green-600' :
                        task.status === 'in_progress' ? 'bg-indigo-50 text-indigo-600' : 'bg-slate-50 text-slate-400'
                    }`}>
                        <CheckSquare size={24} />
                    </div>
                    <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between gap-4 mb-2">
                        <h3 className="font-bold text-slate-800 text-lg truncate group-hover:text-indigo-600 transition duration-300 tracking-tight leading-tight">
                            {task.title}
                        </h3>
                        <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-indigo-400 px-2 py-1 bg-indigo-50 rounded-lg">
                                {projects.find(p => p.id === task.project)?.name}
                            </span>
                            <button className="text-slate-300 hover:text-slate-600 transition shrink-0"><MoreVertical size={20} /></button>
                        </div>
                        </div>
                        <p className="text-slate-500 text-sm line-clamp-2 mb-5 leading-relaxed font-medium">{task.description || 'Без описания'}</p>
                        <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                        <div className="flex items-center gap-1.5"><Calendar size={14} />{task.created_at ? new Date(task.created_at).toLocaleDateString() : '—'}</div>
                        <div className="flex items-center gap-1.5"><Clock size={14} />Исполнитель: {task.assignee || '—'}</div>
                        <div className={`ml-auto px-3 py-1.5 rounded-xl font-black ${
                            task.status === 'done' ? 'bg-green-100 text-green-700' :
                            task.status === 'in_progress' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-100' :
                            'bg-slate-100 text-slate-500'
                        }`}>
                            {task.status}
                        </div>
                        </div>
                    </div>
                    </div>
                ))
                )}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Task Modal */}
      {showTaskModal && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/60 backdrop-blur-md p-4 text-slate-900 overflow-y-auto font-sans">
          <div className="bg-white w-full max-w-xl rounded-[2.5rem] shadow-2xl p-10 animate-in fade-in zoom-in duration-300">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-black tracking-tight text-slate-800">Новая задача</h2>
              <button onClick={() => setShowTaskModal(false)} className="p-3 hover:bg-slate-100 rounded-2xl transition duration-200"><X size={28} className="text-slate-400"/></button>
            </div>

            {formError && (
              <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 text-sm font-bold flex items-center gap-3 rounded-r-xl leading-snug">
                <AlertCircle size={20} className="shrink-0" />
                {formError}
              </div>
            )}

            <form onSubmit={createTask} className="space-y-6">
              <div>
                <label className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-2 px-1">Заголовок</label>
                <input type="text" placeholder="Например: Поправить баг в поиске" required className="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-indigo-500 outline-none transition-all font-bold text-slate-800" value={taskForm.title} onChange={e => setTaskForm({...taskForm, title: e.target.value})} />
              </div>
              <div>
                <label className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-2 px-1">Описание задачи</label>
                <textarea placeholder="Опишите детали..." className="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-indigo-500 outline-none transition-all h-32 font-medium resize-none text-slate-700" value={taskForm.description} onChange={e => setTaskForm({...taskForm, description: e.target.value})} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-2 px-1">Проект</label>
                  <select required className="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-indigo-500 outline-none transition-all font-bold appearance-none cursor-pointer text-slate-800" value={taskForm.project} onChange={e => setTaskForm({...taskForm, project: e.target.value})}>
                    <option value="" disabled>Выбрать...</option>
                    {projects.map(p => <option key={p.id} value={p.id} className="text-slate-800">{p.name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-2 px-1">Статус</label>
                  <select className="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-indigo-500 outline-none transition-all font-bold appearance-none cursor-pointer text-slate-800" value={taskForm.status} onChange={e => setTaskForm({...taskForm, status: e.target.value})}>
                    <option value="new">Новая</option>
                    <option value="in_progress">В работе</option>
                    <option value="done">Завершена</option>
                  </select>
                </div>
              </div>
              <div className="pt-4">
                <button type="submit" className="w-full py-5 bg-indigo-600 text-white font-black text-lg rounded-2xl hover:bg-indigo-700 shadow-2xl shadow-indigo-200 transition-all active:scale-95 duration-200 uppercase tracking-widest">Создать задачу</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Project Modal */}
      {showProjectModal && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/60 backdrop-blur-md p-4 text-slate-900 font-sans">
          <div className="bg-white w-full max-w-xl rounded-[2.5rem] shadow-2xl p-10 animate-in fade-in zoom-in duration-300">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-black tracking-tight text-slate-800">Новый проект</h2>
              <button onClick={() => setShowProjectModal(false)} className="p-3 hover:bg-slate-100 rounded-2xl transition duration-200"><X size={28} className="text-slate-400"/></button>
            </div>

            {formError && (
              <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 text-sm font-bold flex items-center gap-3 rounded-r-xl">
                <AlertCircle size={20} className="shrink-0" />
                {formError}
              </div>
            )}

            <form onSubmit={createProject} className="space-y-6">
              <div>
                <label className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-2 px-1">Название проекта</label>
                <input type="text" placeholder="Напр: Редизайн сайта" required className="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-indigo-500 outline-none transition-all font-bold text-slate-800" value={projectForm.name} onChange={e => setProjectForm({...projectForm, name: e.target.value})} />
              </div>
              <div>
                <label className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-2 px-1">Описание</label>
                <textarea placeholder="О чем этот проект?" className="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-indigo-500 outline-none transition-all h-32 font-medium resize-none text-slate-700" value={projectForm.description} onChange={e => setProjectForm({...projectForm, description: e.target.value})} />
              </div>
              <div className="pt-4">
                <button type="submit" className="w-full py-5 bg-indigo-600 text-white font-black text-lg rounded-2xl hover:bg-indigo-700 shadow-2xl shadow-indigo-200 transition-all active:scale-95 duration-200 uppercase tracking-widest">Создать проект</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
