using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models.Resources
{
    public class MediaModel
    {
        public enum MediaType
        {
            Image,
            Audio,
            Video
        }
        public string Path { get; set; }
        public MediaType Type { get; set; }
        public MediaModel(string path, MediaType type)
        {
            Path = path;
            Type = type;
        }
    }
}
