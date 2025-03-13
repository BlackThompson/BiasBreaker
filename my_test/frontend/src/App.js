import React, { useState, useEffect, useRef } from 'react';
import {
    Container,
    Paper,
    Typography,
    Button,
    Box,
    CircularProgress,
    AppBar,
    Toolbar,
    Alert,
    Avatar,
} from '@mui/material';
import axios from 'axios';

const MessageBubble = ({ message, isUser }) => {
    const bubbleStyle = {
        display: 'flex',
        alignItems: 'flex-start',
        marginBottom: '1rem',
        flexDirection: isUser ? 'row-reverse' : 'row',
    };

    const textBubbleStyle = {
        backgroundColor: isUser ? '#95ec69' : '#ffffff',
        padding: '0.5rem 1rem',
        borderRadius: '1rem',
        maxWidth: '70%',
        marginLeft: isUser ? '0' : '0.5rem',
        marginRight: isUser ? '0.5rem' : '0',
        boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
        wordBreak: 'break-word',
    };

    const avatarStyle = {
        width: 40,
        height: 40,
    };

    return (
        <Box sx={bubbleStyle}>
            <Avatar
                src={message.agent.avatar}
                alt={message.agent.name}
                sx={avatarStyle}
            />
            <Box sx={textBubbleStyle}>
                <Typography variant="body1" component="div">
                    {message.message}
                </Typography>
            </Box>
        </Box>
    );
};

function App() {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const messagesEndRef = useRef(null);
    const eventSourceRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const startConversation = async () => {
        setLoading(true);
        setError(null);
        setMessages([]);

        try {
            // 关闭之前的 EventSource（如果存在）
            if (eventSourceRef.current) {
                eventSourceRef.current.close();
            }

            // 启动对话
            await axios.post('http://localhost:5000/api/start-conversation');

            // 创建新的 EventSource 来接收消息
            const eventSource = new EventSource('http://localhost:5000/api/messages');
            eventSourceRef.current = eventSource;

            eventSource.onmessage = (event) => {
                const message = JSON.parse(event.data);
                setMessages(prev => [...prev, message]);
            };

            eventSource.onerror = () => {
                eventSource.close();
                setLoading(false);
            };
        } catch (error) {
            setError(error.message || '连接服务器失败');
            console.error('Error starting conversation:', error);
            setLoading(false);
        }
    };

    // 清理 EventSource
    useEffect(() => {
        return () => {
            if (eventSourceRef.current) {
                eventSourceRef.current.close();
            }
        };
    }, []);

    return (
        <Box sx={{ flexGrow: 1, height: '100vh', display: 'flex', flexDirection: 'column' }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        多智能体聊天室
                    </Typography>
                </Toolbar>
            </AppBar>

            <Container maxWidth="md" sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', py: 2 }}>
                <Paper
                    elevation={3}
                    sx={{
                        p: 2,
                        flexGrow: 1,
                        display: 'flex',
                        flexDirection: 'column',
                        bgcolor: '#f5f5f5',
                        overflow: 'hidden'
                    }}
                >
                    {error && (
                        <Alert severity="error" sx={{ mb: 2 }}>
                            {error}
                        </Alert>
                    )}

                    <Box sx={{
                        flexGrow: 1,
                        overflow: 'auto',
                        px: 2,
                        '&::-webkit-scrollbar': {
                            width: '8px',
                        },
                        '&::-webkit-scrollbar-track': {
                            backgroundColor: 'transparent',
                        },
                        '&::-webkit-scrollbar-thumb': {
                            backgroundColor: '#bdbdbd',
                            borderRadius: '4px',
                        },
                    }}>
                        {messages.map((msg, index) => (
                            <MessageBubble
                                key={index}
                                message={msg}
                                isUser={msg.agent.name === 'user'}
                            />
                        ))}
                        <div ref={messagesEndRef} />
                    </Box>

                    <Box sx={{
                        mt: 2,
                        pt: 2,
                        borderTop: '1px solid #e0e0e0',
                        display: 'flex',
                        justifyContent: 'center'
                    }}>
                        <Button
                            variant="contained"
                            onClick={startConversation}
                            disabled={loading}
                            sx={{
                                minWidth: 200,
                                bgcolor: '#1aad19',
                                '&:hover': {
                                    bgcolor: '#129611',
                                },
                            }}
                        >
                            {loading ? <CircularProgress size={24} /> : '开始新对话'}
                        </Button>
                    </Box>
                </Paper>
            </Container>
        </Box>
    );
}

export default App; 