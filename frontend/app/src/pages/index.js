// pages/index.js
import { useState } from 'react';
import { Button } from 'primereact/button';
import CreateRoom from '@/components/CreateRoom';
import JoinRoom from '@/components/JoinRoom';

const HomePage = () => {
  const [createDialog, setCreateDialog] = useState(false);
  const [joinDialog, setJoinDialog] = useState(false);

  return (
    <div>
      <div
        className='p-d-flex p-ai-center p-jc-center'
        style={{ height: '10vh', textAlign: 'center' }}
      >
        <h1>Planning Poker</h1>
        <Button
          label='Create Room'
          onClick={() => setCreateDialog(true)}
          style={{ marginRight: '5px' }}
        />
        <Button label='Join Room' onClick={() => setJoinDialog(true)} />
      </div>

      <CreateRoom
        visible={createDialog}
        onHide={() => setCreateDialog(false)}
      />
      <JoinRoom visible={joinDialog} onHide={() => setJoinDialog(false)} />
    </div>
  );
};

export default HomePage;
