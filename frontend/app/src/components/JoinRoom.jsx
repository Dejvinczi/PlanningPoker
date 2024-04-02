import React, { useState, useRef } from 'react';
import { useRouter } from 'next/router';
import { Toast } from 'primereact/toast';
import { Dialog } from 'primereact/dialog';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import api from '@/api/root';

const JoinRoom = ({ visible, onHide }) => {
  const router = useRouter();
  const [roomId, setRoomId] = useState('');
  const [password, setPassword] = useState('');
  const [voter, setVoter] = useState('');
  const [errors, setErrors] = useState({});
  const toast = useRef(null);

  const showToast = (type, title, detail) => {
    toast.current.show({
      severity: type,
      summary: title,
      detail: detail,
      life: 3000,
    });
  };

  const handleSubmit = async () => {
    setErrors({});
    try {
      const response = await api.post('join-room', {
        room: roomId,
        password,
        voter,
      });
      showToast('success', 'Joined the room', `Voter ID: ${response.data.id}`);
      hideDialog();
      router.push(`/${roomId}`);
    } catch (error) {
      if (error.response) {
        if (error.response.status === 400) setErrors(error.response.data);
        else showToast('error', 'Error', `Status ${error.response.status}`);
      } else showToast('error', 'Error', `Something went wrong`);

      return null;
    }
  };

  const hideDialog = () => {
    setRoomId('');
    setPassword('');
    setVoter('');
    setErrors({});
    onHide();
  };

  return (
    <div>
      <Toast ref={toast} position='top-right' />
      <Dialog
        header='Join Room'
        visible={visible}
        onHide={hideDialog}
        modal
        position='top'
        draggable={false}
        footer={<Button label='Join' onClick={handleSubmit} />}
        style={{ width: '50vw' }}
      >
        <div
          style={{
            marginBottom: '5px',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <InputText
            id='room'
            placeholder='Room ID'
            value={roomId}
            onChange={(e) => setRoomId(e.target.value)}
            className={errors.room ? 'p-invalid' : ''}
          />
          {errors.room && <small className='p-error'>{errors.room}</small>}
        </div>
        <div
          style={{
            marginBottom: '5px',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <InputText
            id='password'
            placeholder='Room password'
            type='password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={errors.password ? 'p-invalid' : ''}
          />
          {errors.password && (
            <small className='p-error'>{errors.password}</small>
          )}
        </div>
        <div
          style={{
            marginBottom: '5px',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <InputText
            id='voter'
            placeholder='Voter name'
            value={voter}
            onChange={(e) => setVoter(e.target.value)}
            className={errors.voter ? 'p-invalid' : ''}
          />
          {errors.voter && (
            <div>
              <small className='p-error'>{errors.voter}</small>
            </div>
          )}
        </div>
      </Dialog>
    </div>
  );
};

export default JoinRoom;
