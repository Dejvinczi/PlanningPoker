import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/router';
import { Toast } from 'primereact/toast';
import JoinRoom from '@/components/JoinRoom';
import Game from '@/components/Game';

const GamePage = () => {
  const [joinDialog, setJoinDialog] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [voterId, setVoterId] = useState(null);
  const router = useRouter();
  const toast = useRef(null);

  useEffect(() => {
    const { roomId } = router.query;
    if (!roomId) return;

    const roomStorageData = JSON.parse(localStorage.getItem(roomId));

    if (roomStorageData) {
      setIsAdmin(roomStorageData.isAdmin);
      setVoterId(roomStorageData.voterId);
    } else {
      setJoinDialog(true);
    }
  }, [router.query]);

  return (
    <div>
      <Toast ref={toast} />
      <JoinRoom visible={joinDialog} onHide={() => setJoinDialog(false)} />
      {(isAdmin || voterId) && (
        <Game
          roomId={router.query.roomId}
          isAdmin={isAdmin}
          voterId={voterId}
          toastRef={toast}
        />
      )}
    </div>
  );
};

export default GamePage;
