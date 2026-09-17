using Godot;
using Satsuki.Models;
using Satsuki.Networks;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes.Abstract
{
    public partial class GameScene : Node
    {
        MessageHandler messageHandler = MessageHandler.GetInstance;
        Queue<OrderRequest> messageQueue = new Queue<OrderRequest>();

        public void OnMessageReceived(OrderRequest orderRequest)
        {
            messageQueue.Enqueue(orderRequest);
        }
    }
}
