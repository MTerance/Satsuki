using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Utils
{

    public abstract class SingletonBase<T>
        where T : SingletonBase<T>, new()
    {
        static private T _instance = null;

        static public T GetInstance
        {
            get
            {
                if (_instance == null)
                    _instance = new T();
                return _instance;
            }
        }
    }
}
